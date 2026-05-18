"""Request builders for authentication APIs."""

from dataclasses import dataclass, field

from core.framework.types import LoginPayload


@dataclass(slots=True)
class AuthRequest:
    request_body: LoginPayload = field(default_factory=lambda: {"username": "", "password": ""})

    def login_request(self, username: str, password: str) -> "AuthRequest":
        self.request_body = {
            "username": username,
            "password": password,
        }
        return self
