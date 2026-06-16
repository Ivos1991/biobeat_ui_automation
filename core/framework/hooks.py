"""Typed hook manager with ordered execution and failure isolation."""

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Protocol

from core.framework.types import HookName, Metadata, TestId


@dataclass(slots=True)
class SessionContext:
    session_id: str
    settings: object
    metadata: Metadata = field(default_factory=dict)


@dataclass(slots=True)
class TestContext:
    test_id: TestId
    nodeid: str
    name: str
    phase: str = "call"
    outcome: str | None = None
    metadata: Metadata = field(default_factory=dict)


@dataclass(slots=True)
class StepContext:
    test: TestContext
    step_name: str
    metadata: Metadata = field(default_factory=dict)


@dataclass(slots=True)
class ApiCallContext:
    client_name: str
    method: str
    url: str
    expected_statuses: tuple[int, ...]
    status_code: int | None = None
    duration_ms: float | None = None
    request_kwargs: Metadata = field(default_factory=dict)
    response_payload: Any | None = None
    error: BaseException | None = None
    metadata: Metadata = field(default_factory=dict)


@dataclass(slots=True)
class FailureContext:
    test: TestContext
    error: BaseException | None = None
    report: Any | None = None
    metadata: Metadata = field(default_factory=dict)


HookContext = SessionContext | TestContext | StepContext | ApiCallContext | FailureContext


class HookHandler(Protocol):
    def __call__(self, context: HookContext) -> None: ...


@dataclass(order=True, slots=True)
class RegisteredHook:
    order: int
    name: HookName
    callback: HookHandler
    owner: str
    critical: bool = False


class HookManager:
    """Registers and executes framework lifecycle hooks."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger
        self._handlers: dict[HookName, list[RegisteredHook]] = {
            name: []
            for name in (
                "before_session",
                "after_session",
                "before_test",
                "after_test",
                "before_step",
                "after_step",
                "on_failure",
                "before_api_call",
                "after_api_call",
            )
        }

    def register(
        self,
        name: HookName,
        callback: HookHandler,
        *,
        order: int = 100,
        owner: str = "framework",
        critical: bool = False,
    ) -> None:
        self._handlers[name].append(
            RegisteredHook(order=order, name=name, callback=callback, owner=owner, critical=critical)
        )
        self._handlers[name].sort()

    def emit(self, name: HookName, context: HookContext) -> list[BaseException]:
        failures: list[BaseException] = []
        for handler in self._handlers[name]:
            started = perf_counter()
            try:
                handler.callback(context)
            except BaseException as error:
                failures.append(error)
                self._logger.exception(
                    "Hook '%s' failed in handler '%s' (critical=%s)",
                    name,
                    handler.owner,
                    handler.critical,
                )
                if handler.critical:
                    raise
            finally:
                duration_ms = (perf_counter() - started) * 1000
                self._logger.debug(
                    "Hook '%s' handled by '%s' in %.2fms",
                    name,
                    handler.owner,
                    duration_ms,
                )
        return failures
