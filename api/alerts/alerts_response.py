"""Response models for alert APIs."""

from dataclasses import dataclass

from core.framework.types import AlertId


@dataclass(slots=True)
class AssigneeResponse:
    id: str
    name: str
    email: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "AssigneeResponse":
        return cls(
            id=data["id"],
            name=data["name"],
            email=data.get("email"),
        )


@dataclass(slots=True)
class AlertCommentResponse:
    id: str
    author_name: str
    message: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "AlertCommentResponse":
        return cls(
            id=data["id"],
            author_name=data["author"]["name"],
            message=data["message"],
            created_at=data["createdAt"],
        )


@dataclass(slots=True)
class PolicySnapshotResponse:
    violation_type: str | None
    auto_remediate: bool
    remediation_type: str | None
    remediation_priority: str | None
    remediation_due: str | None
    supported_assets: list[str] | None

    @classmethod
    def from_dict(cls, data: dict | None) -> "PolicySnapshotResponse":
        payload = data or {}
        return cls(
            violation_type=payload.get("violationType"),
            auto_remediate=bool(payload.get("autoRemediate", False)),
            remediation_type=payload.get("remediationType"),
            remediation_priority=payload.get("remediationPriority"),
            remediation_due=payload.get("remediationDue"),
            supported_assets=payload.get("supportedAssets"),
        )


@dataclass(slots=True)
class AlertResponse:
    id: AlertId
    run_id: str
    policy_id: str
    policy_name: str
    severity: str
    created_severity: str
    status: str
    description: str
    violation_type: str
    asset_display_name: str
    asset_location: str
    was_remediated: bool
    remediation_origin: str
    assigned_to: AssigneeResponse | None
    comments: tuple[AlertCommentResponse, ...]
    created_at: str
    updated_at: str | None
    valid_transitions: tuple[str, ...]
    can_remediate: bool
    policy_snapshot: PolicySnapshotResponse

    @classmethod
    def from_dict(cls, data: dict) -> "AlertResponse":
        return cls(
            id=AlertId(data["id"]),
            run_id=data["runId"],
            policy_id=data["policyId"],
            policy_name=data["policyName"],
            severity=data["severity"],
            created_severity=data.get("createdSeverity", data["severity"]),
            status=data["status"],
            description=data["description"],
            violation_type=data["violationType"],
            asset_display_name=data.get("assetDisplayName") or data["asset"]["metadata"]["name"],
            asset_location=data.get("assetLocation") or data["asset"]["location"],
            was_remediated=bool(data.get("wasRemediated", False)),
            remediation_origin=data.get("remediationOrigin", "NONE"),
            assigned_to=AssigneeResponse.from_dict(data["assignedTo"]) if data.get("assignedTo") else None,
            comments=tuple(AlertCommentResponse.from_dict(item) for item in data.get("comments", [])),
            created_at=data["createdAt"],
            updated_at=data.get("updatedAt"),
            valid_transitions=tuple(data.get("validTransitions", [])),
            can_remediate=bool(data.get("canRemediate", False)),
            policy_snapshot=PolicySnapshotResponse.from_dict(data.get("policySnapshot")),
        )

    def matches_signature(self, other: "AlertResponse") -> bool:
        return (
            self.policy_id == other.policy_id
            and self.asset_location == other.asset_location
            and self.violation_type == other.violation_type
            and self.created_severity == other.created_severity
        )
