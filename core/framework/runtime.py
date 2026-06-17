"""Framework bootstrapper that wires settings, hooks, plugins, and shared services."""

import uuid
from dataclasses import dataclass
from typing import Any

from config.settings import Settings
from core.core_utils.logger import configure_logging, get_logger
from core.framework.hooks import HookManager, SessionContext
from core.framework.plugins import PluginManager


@dataclass(slots=True)
class FrameworkRuntime:
    """Top-level runtime object shared across pytest fixtures and hooks."""

    settings: Settings
    hooks: HookManager
    plugins: PluginManager
    logger: Any
    session_context: SessionContext


def build_runtime(settings: Settings | None = None) -> FrameworkRuntime:
    """Build and wire the framework runtime."""

    resolved_settings = settings or Settings.from_env()
    # Logging is configured first so every later bootstrap step can emit diagnostics.
    configure_logging(resolved_settings.reporting.log_dir, resolved_settings.runtime.log_level)
    logger = get_logger("framework")
    hooks = HookManager(logger)
    plugins = PluginManager(logger)
    # The session context carries run-level metadata across hooks and plugins.
    session_context = SessionContext(session_id=str(uuid.uuid4()), settings=resolved_settings)

    runtime = FrameworkRuntime(
        settings=resolved_settings,
        hooks=hooks,
        plugins=plugins,
        logger=logger,
        session_context=session_context,
    )

    # Plugin activation can register lifecycle hooks before the test session starts.
    plugins.activate(runtime, resolved_settings.plugins.enabled)
    hooks.emit("before_session", session_context)
    return runtime
