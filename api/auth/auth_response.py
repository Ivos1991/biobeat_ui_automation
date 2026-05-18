"""Response models for authentication APIs."""

from dataclasses import dataclass


@dataclass(slots=True)
class AuthUserResponse:
    id: str
    display_name: str
    role: str

    @classmethod
    def from_dict(cls, data: dict) -> "AuthUserResponse":
        return cls(
            id=data["id"],
            display_name=data["displayName"],
            role=data["role"],
        )


@dataclass(slots=True)
class AuthResponse:
    token: str
    user: AuthUserResponse

    @classmethod
    def from_dict(cls, data: dict) -> "AuthResponse":
        return cls(
            token=data["token"],
            user=AuthUserResponse.from_dict(data["user"]),
        )
