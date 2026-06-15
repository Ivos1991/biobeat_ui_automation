"""Framework bootstrapper that wires settings, hooks, plugins, and shared services."""

import uuid
from dataclasses import dataclass
from typing import Any

from config.settings import Settings
from core.core_utils.logger import configure_logging, get_logger
from core.framework.container import ServiceContainer
from core.framework.hooks import HookManager, SessionContext
from core.framework.plugins import PluginManager


@dataclass(slots=True)
class FrameworkRuntime:
    """Top-level runtime object shared across pytest fixtures and hooks."""

    settings: Settings
    container: ServiceContainer
    hooks: HookManager
    plugins: PluginManager
    logger: Any
    session_context: SessionContext


def build_runtime(settings: Settings | None = None) -> FrameworkRuntime:
    """Build and wire the framework runtime."""

    resolved_settings = settings or Settings.from_env()
    configure_logging(resolved_settings.reporting.log_dir, resolved_settings.runtime.log_level)
    logger = get_logger("framework")
    hooks = HookManager(logger)
    plugins = PluginManager(logger)
    container = ServiceContainer()
    session_context = SessionContext(session_id=str(uuid.uuid4()), settings=resolved_settings)

    runtime = FrameworkRuntime(
        settings=resolved_settings,
        container=container,
        hooks=hooks,
        plugins=plugins,
        logger=logger,
        session_context=session_context,
    )

    container.register_singleton(FrameworkRuntime, instance=runtime)
    container.register_singleton(Settings, instance=resolved_settings)
    container.register_singleton(HookManager, instance=hooks)
    container.register_singleton(PluginManager, instance=plugins)

    plugins.activate(runtime, resolved_settings.plugins.enabled)
    hooks.emit("before_session", session_context)
    return runtime
