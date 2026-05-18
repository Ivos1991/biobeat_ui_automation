"""Polling and retry utilities shared across the framework."""

import time
from collections.abc import Callable
from typing import TypeVar

from core.exceptions import PollTimeoutError


T = TypeVar("T")


def wait_until(predicate: Callable[[], T | None], *, timeout_seconds: float, interval_seconds: float, description: str) -> T:
    """Poll ``predicate`` until it returns a truthy value or timeout expires."""

    deadline = time.monotonic() + timeout_seconds
    last_value: T | None = None

    while time.monotonic() < deadline:
        last_value = predicate()
        if last_value:
            return last_value
        time.sleep(interval_seconds)

    raise PollTimeoutError(
        f"Timed out after {timeout_seconds}s while waiting for {description}. Last value: {last_value!r}"
    )
