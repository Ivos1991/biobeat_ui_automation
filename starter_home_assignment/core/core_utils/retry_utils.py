import time
from typing import Callable, TypeVar

from core.exceptions import PollTimeoutError


T = TypeVar("T")


def wait_until(predicate: Callable[[], T], *, timeout_seconds: float, interval_seconds: float, description: str) -> T:
    deadline = time.time() + timeout_seconds
    last_value: T | None = None

    while time.time() < deadline:
        last_value = predicate()
        if last_value:
            return last_value
        time.sleep(interval_seconds)

    raise PollTimeoutError(
        f"Timed out after {timeout_seconds}s while waiting for {description}. Last value: {last_value!r}"
    )
