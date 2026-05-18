"""Response models for scan APIs."""

from dataclasses import dataclass

from core.framework.types import ScanId


@dataclass(slots=True)
class ScanResponse:
    id: ScanId
    status: str
    started_at: str
    completed_at: str | None
    scanned_assets_count: int
    alerts_created_count: int

    @classmethod
    def from_dict(cls, data: dict) -> "ScanResponse":
        return cls(
            id=ScanId(data["id"]),
            status=data["status"],
            started_at=data["startedAt"],
            completed_at=data.get("completedAt"),
            scanned_assets_count=data["scannedAssetsCount"],
            alerts_created_count=data["alertsCreatedCount"],
        )
