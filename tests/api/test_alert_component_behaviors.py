import pytest
from assertpy import assert_that
from core.exceptions import ApiRequestError
from core.framework.types import AlertStatus


@pytest.mark.api
@pytest.mark.component
def test_open_alert_status_transition_expects_rejected_direct_resolve(alert_workflows, alerts_service):
    alert = alert_workflows.create_manual_alert().alert

    with pytest.raises(ApiRequestError) as exc_info:
        alerts_service.update_alert(alert.id, status=AlertStatus.RESOLVED)

    assert_that(exc_info.value.status_code).described_as("invalid status transition response code").is_equal_to(400)
    assert_that(exc_info.value.response_text or "").described_as("invalid transition response body").contains(
        "Invalid status transition"
    )
