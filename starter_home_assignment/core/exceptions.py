class FrameworkError(Exception):
    """Base exception for the framework."""


class ApiRequestError(FrameworkError):
    """Raised when an API request returns an unexpected status."""

    def __init__(self, message: str, status_code: int, response_text: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class PollTimeoutError(FrameworkError):
    """Raised when polling exceeds the configured timeout."""
