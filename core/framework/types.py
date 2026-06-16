"""Shared type contracts used across the framework runtime."""

from enum import StrEnum
from typing import Any, Literal, NewType

TestId = NewType("TestId", str)
PluginName = NewType("PluginName", str)

BrowserName = Literal["chromium", "firefox", "webkit"]
EvidenceMode = Literal["full", "failure_only", "screenshot_only"]
HookName = Literal[
    "before_session",
    "after_session",
    "before_test",
    "after_test",
    "before_step",
    "after_step",
    "on_failure",
    "before_api_call",
    "after_api_call",
]


class Environment(StrEnum):
    """Supported framework execution environments."""

    LOCAL = "local"
    CI = "ci"
    QA = "qa"


Metadata = dict[str, Any]
