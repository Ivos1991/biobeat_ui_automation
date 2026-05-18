"""Response models for admin APIs."""

from dataclasses import dataclass


@dataclass(slots=True)
class ResetEnvironmentResponse:
    success: bool
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "ResetEnvironmentResponse":
        return cls(
            success=bool(data["success"]),
            message=data["message"],
        )
