"""Framework bootstrapper that wires settings, hooks, plugins, and services."""

import uuid
from dataclasses import dataclass
from typing import Any

from api.admin.admin_api import AdminApi
from api.admin.admin_service import AdminService
from api.alerts.alerts_api import AlertsApi
from api.alerts.alerts_service import AlertsService
from api.auth.auth_api import AuthApi
from api.auth.auth_service import AuthService
from api.scans.scans_api import ScansApi
from api.scans.scans_service import ScansService
from api.system.system_api import SystemApi
from api.system.system_service import SystemService
from config.settings import Settings
from core.core_utils.logger import configure_logging, get_logger
from core.framework.container import ServiceContainer
from core.framework.hooks import HookManager, SessionContext
from core.framework.plugins import PluginManager
from core.orchestrators.alert_workflows import AlertWorkflowOrchestrator


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

    container.register_singleton(AuthApi, lambda c: AuthApi(c.typed_resolve(Settings, Settings), runtime=runtime))
    container.register_singleton(AuthService, lambda c: AuthService(c.typed_resolve(AuthApi, AuthApi)))

    container.register_singleton(AdminApi, lambda c: AdminApi(c.typed_resolve(Settings, Settings), runtime=runtime))
    container.register_singleton(AdminService, lambda c: AdminService(c.typed_resolve(AdminApi, AdminApi)))

    container.register_singleton(AlertsApi, lambda c: AlertsApi(c.typed_resolve(Settings, Settings), runtime=runtime))
    container.register_singleton(
        AlertsService,
        lambda c: AlertsService(c.typed_resolve(AlertsApi, AlertsApi), c.typed_resolve(Settings, Settings)),
    )

    container.register_singleton(ScansApi, lambda c: ScansApi(c.typed_resolve(Settings, Settings), runtime=runtime))
    container.register_singleton(
        ScansService, lambda c: ScansService(c.typed_resolve(ScansApi, ScansApi), c.typed_resolve(Settings, Settings))
    )
    container.register_singleton(
        AlertWorkflowOrchestrator,
        lambda c: AlertWorkflowOrchestrator(
            c.typed_resolve(ScansService, ScansService), c.typed_resolve(AlertsService, AlertsService)
        ),
    )

    container.register_singleton(SystemApi, lambda c: SystemApi(c.typed_resolve(Settings, Settings), runtime=runtime))
    container.register_singleton(SystemService, lambda c: SystemService(c.typed_resolve(SystemApi, SystemApi)))

    plugins.activate(runtime, resolved_settings.plugins.enabled)
    hooks.emit("before_session", session_context)
    return runtime
