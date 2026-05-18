"""Request builders for alert management APIs."""

from dataclasses import dataclass, field

from core.framework.types import AlertCommentPayload, AlertUpdatePayload, RemediationPayload


@dataclass(slots=True)
class AlertsRequest:
    request_body: AlertUpdatePayload | AlertCommentPayload | RemediationPayload = field(default_factory=dict)

    def update_alert_request(self, *, status: str | None = None, severity: str | None = None, assigned_to_id: str | None = None) -> "AlertsRequest":
        payload: AlertUpdatePayload = {}
        if status is not None:
            payload["status"] = status
        if severity is not None:
            payload["severity"] = severity
        if assigned_to_id is not None:
            payload["assignedToId"] = assigned_to_id
        self.request_body = payload
        return self

    def add_comment_request(self, message: str) -> "AlertsRequest":
        self.request_body = {"message": message}
        return self

    def remediate_request(self, note: str | None = None) -> "AlertsRequest":
        payload: RemediationPayload = {}
        if note:
            payload["note"] = note
        self.request_body = payload
        return self
