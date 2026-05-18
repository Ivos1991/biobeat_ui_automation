"""Shared type contracts used across the framework runtime."""

from enum import Enum
from typing import Any, Literal, NewType, TypedDict


AlertId = NewType("AlertId", str)
ScanId = NewType("ScanId", str)
TestId = NewType("TestId", str)
PluginName = NewType("PluginName", str)

EvidenceMode = Literal["off", "failure_only", "full_evidence"]
HookName = Literal[
    "before_session",
    "after_session",
    "before_test",
    "after_test",
    "before_step",
    "after_step",
    "on_failure",
    "before_api_call",
    "after_api_call",
]


class Environment(str, Enum):
    """Supported framework execution environments."""

    LOCAL = "local"
    CI = "ci"
    QA = "qa"


class AlertStatus(str, Enum):
    """Backend alert statuses used across API and UI flows."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    REMEDIATION_IN_PROGRESS = "REMEDIATION_IN_PROGRESS"
    REMEDIATED_WAITING_FOR_CUSTOMER = "REMEDIATED_WAITING_FOR_CUSTOMER"
    RESOLVED = "RESOLVED"


class ScanStatus(str, Enum):
    """Supported scan states returned by the API."""

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"


class LoginPayload(TypedDict):
    """Request payload for authentication."""

    username: str
    password: str


class AlertUpdatePayload(TypedDict, total=False):
    """PATCH payload for alert updates."""

    status: str
    severity: str
    assignedToId: str


class AlertCommentPayload(TypedDict):
    """Request payload for adding a comment to an alert."""

    message: str


class RemediationPayload(TypedDict, total=False):
    """Request payload for starting remediation."""

    note: str


Metadata = dict[str, Any]
