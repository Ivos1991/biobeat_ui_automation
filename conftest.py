"""Global pytest configuration and framework bootstrap."""

from pathlib import Path
from typing import Any
import pytest
from assertpy import assert_that
from api.admin.admin_api import AdminApi
from api.admin.admin_service import AdminService
from api.alerts.alerts_api import AlertsApi
from api.alerts.alerts_service import AlertsService
from api.auth.auth_api import AuthApi
from api.auth.auth_service import AuthService
from api.scans.scans_api import ScansApi
from api.scans.scans_service import ScansService
from config.settings import Settings
from core.framework.hooks import FailureContext, TestContext
from core.framework.runtime import FrameworkRuntime, build_runtime
from core.framework.types import TestId
from core.orchestrators.alert_workflows import AlertWorkflowOrchestrator
from ui.page_factory import PageObjectFactory


def _runtime(config: pytest.Config) -> FrameworkRuntime:
    runtime = getattr(config, "_framework_runtime", None)
    if runtime is None:
        runtime = build_runtime()
        setattr(config, "_framework_runtime", runtime)
    return runtime


def _apply_playwright_artifact_defaults(config: pytest.Config, items: list[pytest.Item]) -> None:
    runtime = _runtime(config)
    mode = runtime.settings.browser_evidence_mode
    has_collect_all_marker = any(item.get_closest_marker("collect_all_evidence") for item in items)
    force_always = mode == "full_evidence" or has_collect_all_marker

    if getattr(config.option, "output", None) == "test-results":
        config.option.output = str(Path(runtime.settings.artifact_dir) / "playwright")

    if mode == "off":
        return

    if getattr(config.option, "screenshot", None) == "off":
        config.option.screenshot = "on" if force_always else "only-on-failure"

    if getattr(config.option, "video", None) == "off":
        config.option.video = "on" if force_always else "retain-on-failure"

    if getattr(config.option, "tracing", None) == "off":
        config.option.tracing = "on" if force_always else "retain-on-failure"


def pytest_configure(config: pytest.Config) -> None:
    _runtime(config)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    _apply_playwright_artifact_defaults(config, items)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    runtime = _runtime(session.config)
    runtime.session_context.metadata["exitstatus"] = exitstatus
    runtime.hooks.emit("after_session", runtime.session_context)


def pytest_runtest_setup(item: pytest.Item) -> None:
    runtime = _runtime(item.config)
    context = TestContext(test_id=TestId(item.nodeid), nodeid=item.nodeid, name=item.name, phase="setup")
    setattr(item, "_framework_test_context", context)
    runtime.session_context.metadata["current_test"] = context
    runtime.hooks.emit("before_test", context)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    runtime = _runtime(item.config)
    context = getattr(item, "_framework_test_context", None)
    if not isinstance(context, TestContext):
        return

    context.phase = report.when
    if report.when == "call":
        context.outcome = report.outcome
        if report.failed:
            runtime.hooks.emit(
                "on_failure",
                FailureContext(test=context, error=call.excinfo.value if call.excinfo else None, report=report),
            )
        runtime.hooks.emit("after_test", context)
        runtime.session_context.metadata.pop("current_test", None)


@pytest.fixture(scope="session")
def framework(pytestconfig: pytest.Config) -> FrameworkRuntime:
    return _runtime(pytestconfig)


@pytest.fixture(scope="session")
def service_container(framework: FrameworkRuntime):
    return framework.container


@pytest.fixture(scope="session")
def settings(framework: FrameworkRuntime) -> Settings:
    return framework.settings


@pytest.fixture(scope="session")
def logger(framework: FrameworkRuntime):
    return framework.logger


@pytest.fixture(scope="session")
def page_factory(framework: FrameworkRuntime, settings: Settings) -> PageObjectFactory:
    return PageObjectFactory(settings=settings, runtime=framework)


@pytest.fixture(scope="session")
def auth_api(service_container) -> AuthApi:
    return service_container.typed_resolve(AuthApi, AuthApi)


@pytest.fixture(scope="session")
def auth_service(service_container) -> AuthService:
    return service_container.typed_resolve(AuthService, AuthService)


@pytest.fixture(scope="session")
def authenticated_api(auth_service: AuthService, settings: Settings):
    response = auth_service.login(settings.username, settings.password)
    assert_that(response.user.role).described_as("authenticated user role").is_equal_to("ADMIN")
    return response


@pytest.fixture(scope="session")
def admin_api(service_container, authenticated_api) -> AdminApi:
    api = service_container.typed_resolve(AdminApi, AdminApi)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def admin_service(service_container, admin_api: AdminApi) -> AdminService:
    service = service_container.typed_resolve(AdminService, AdminService)
    service.admin_api = admin_api
    return service


@pytest.fixture(scope="session")
def alerts_api(service_container, authenticated_api) -> AlertsApi:
    api = service_container.typed_resolve(AlertsApi, AlertsApi)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def alerts_service(service_container, alerts_api: AlertsApi) -> AlertsService:
    service = service_container.typed_resolve(AlertsService, AlertsService)
    service.alerts_api = alerts_api
    return service


@pytest.fixture(scope="session")
def scans_api(service_container, authenticated_api) -> ScansApi:
    api = service_container.typed_resolve(ScansApi, ScansApi)
    api.set_token(authenticated_api.token)
    return api


@pytest.fixture(scope="session")
def scans_service(service_container, scans_api: ScansApi) -> ScansService:
    service = service_container.typed_resolve(ScansService, ScansService)
    service.scans_api = scans_api
    return service


@pytest.fixture(scope="session")
def alert_workflows(service_container, scans_service: ScansService, alerts_service: AlertsService) -> AlertWorkflowOrchestrator:
    orchestrator = service_container.typed_resolve(AlertWorkflowOrchestrator, AlertWorkflowOrchestrator)
    orchestrator.scans_service = scans_service
    orchestrator.alerts_service = alerts_service
    return orchestrator
