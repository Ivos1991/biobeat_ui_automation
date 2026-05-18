"""Response models for system APIs."""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class HealthResponse:
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HealthResponse":
        return cls(data=data)
