"""Alert orchestration service layer."""

from collections.abc import Iterable

from assertpy import assert_that

from api.alerts.alerts_api import AlertsApi
from api.alerts.alerts_request import AlertsRequest
from api.alerts.alerts_response import AlertCommentResponse, AlertResponse
from config.settings import Settings
from core.core_utils.logger import get_logger
from core.core_utils.retry_utils import wait_until
from core.framework.decorators import logged_call, timed_call
from core.framework.types import AlertId, AlertStatus


class AlertsService:
    """Business service for alert workflows and polling."""

    def __init__(self, alerts_api: AlertsApi, settings: Settings) -> None:
        self.alerts_api = alerts_api
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)

    def list_alerts(self, **filters: str) -> list[AlertResponse]:
        return [AlertResponse.from_dict(item) for item in self.alerts_api.list_alerts(**filters) or []]

    def get_alert(self, alert_id: AlertId | str) -> AlertResponse:
        return AlertResponse.from_dict(self.alerts_api.get_alert(str(alert_id)))

    @logged_call("Update alert")
    @timed_call("alerts.update_alert")
    def update_alert(self, alert_id: AlertId | str, *, status: str | AlertStatus | None = None, severity: str | None = None, assigned_to_id: str | None = None) -> AlertResponse:
        status_value = status.value if isinstance(status, AlertStatus) else status
        request_body = AlertsRequest().update_alert_request(
            status=status_value,
            severity=severity,
            assigned_to_id=assigned_to_id,
        ).request_body
        response = AlertResponse.from_dict(self.alerts_api.update_alert(str(alert_id), request_body))
        if status_value is not None:
            assert_that(response.status).described_as("updated alert status").is_equal_to(status_value)
        if assigned_to_id is not None:
            assert_that(response.assigned_to).described_as("updated alert assignee should exist").is_not_none()
        return response

    @logged_call("Add alert comment")
    @timed_call("alerts.add_comment")
    def add_comment(self, alert_id: AlertId | str, message: str) -> AlertCommentResponse:
        request_body = AlertsRequest().add_comment_request(message).request_body
        response = AlertCommentResponse.from_dict(self.alerts_api.add_comment(str(alert_id), request_body))
        assert_that(response.message).described_as("alert comment message").is_equal_to(message)
        return response

    @logged_call("Start alert remediation")
    @timed_call("alerts.start_remediation")
    def start_remediation(self, alert_id: AlertId | str, note: str | None = None) -> AlertResponse:
        request_body = AlertsRequest().remediate_request(note).request_body
        response = AlertResponse.from_dict(self.alerts_api.remediate_alert(str(alert_id), request_body))
        assert_that(response.status).described_as("alert status after remediation start").is_equal_to(
            AlertStatus.REMEDIATION_IN_PROGRESS.value
        )
        return response

    @logged_call("Wait for alert status")
    @timed_call("alerts.wait_for_status")
    def wait_for_status(self, alert_id: AlertId | str, expected_statuses: Iterable[str | AlertStatus]) -> AlertResponse:
        expected = {status.value if isinstance(status, AlertStatus) else status for status in expected_statuses}

        def _fetch() -> AlertResponse | None:
            alert = self.get_alert(alert_id)
            return alert if alert.status in expected else None

        response = wait_until(
            _fetch,
            timeout_seconds=self.settings.poll_timeout_seconds,
            interval_seconds=self.settings.poll_interval_seconds,
            description=f"alert {alert_id} to reach one of {sorted(expected)}",
        )
        assert_that(response.status).described_as("polled alert final status").is_in(*expected)
        return response

    def find_alert(self, *, statuses: Iterable[str | AlertStatus], auto_remediate: bool) -> AlertResponse:
        allowed_statuses = {status.value if isinstance(status, AlertStatus) else status for status in statuses}
        candidates = self.list_alerts()
        for alert in candidates:
            if alert.status not in allowed_statuses:
                continue
            if alert.policy_snapshot.auto_remediate is auto_remediate:
                return alert
        assert_that(candidates).described_as("available alerts after scan").is_not_empty()
        raise AssertionError(
            f"No alert found for statuses={sorted(allowed_statuses)} and auto_remediate={auto_remediate}. "
            f"Available alerts={[(a.id, a.status, a.policy_snapshot.auto_remediate) for a in candidates]}"
        )
