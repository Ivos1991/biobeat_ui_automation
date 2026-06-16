"""Global pytest configuration and framework bootstrap."""

from __future__ import annotations

from pathlib import Path
from types import MethodType
from typing import Any

import allure
import allure_commons
import pytest
from playwright.sync_api import Page
from allure_commons.model2 import TestBeforeResult, TestResultContainer
from allure_commons.utils import now, uuid4
from allure_pytest.utils import get_outcome_status, get_outcome_status_details

from config.settings import Settings
from core.framework.hooks import FailureContext, TestContext
from core.framework.runtime import FrameworkRuntime, build_runtime
from core.framework.types import TestId
from core.reporting import write_allure_environment
from core.testing_utils.evidence import (
    should_attach_test_evidence,
    should_capture_trace,
    should_record_video,
)
from core.testing_utils.playwright_artifacts import (
    attach_artifacts_from_output_path,
    attach_log_file,
    attach_page_screenshot,
)
from ui.page_factory import PageObjectFactory

ALLURE_REPORTED_FIXTURES = {"attach_ui_artifacts"}


def _runtime(config: pytest.Config) -> FrameworkRuntime:
    runtime = getattr(config, "_framework_runtime", None)
    if runtime is None:
        runtime = build_runtime()
        config._framework_runtime = runtime
    return runtime


def _apply_playwright_defaults(config: pytest.Config, items: list[pytest.Item]) -> None:
    runtime = _runtime(config)
    settings = runtime.settings
    collect_all_requested = any(item.get_closest_marker("collect_all_evidence") for item in items)

    if getattr(config.option, "browser", None) in (None, []):
        config.option.browser = [settings.browser_name]

    if getattr(config.option, "output", None) == "test-results":
        config.option.output = str(Path(settings.artifact_dir) / "playwright")

    if getattr(config.option, "screenshot", None) == "off":
        config.option.screenshot = (
            "on"
            if collect_all_requested or settings.browser_evidence_mode == "full"
            else "only-on-failure"
        )

    if getattr(config.option, "video", None) == "off":
        config.option.video = (
            "on"
            if collect_all_requested or settings.browser_evidence_mode == "full"
            else "retain-on-failure"
            if should_record_video(settings.browser_evidence_mode, collect_all_requested)
            else "off"
        )

    if getattr(config.option, "tracing", None) == "off":
        config.option.tracing = (
            "on"
            if collect_all_requested or settings.browser_evidence_mode == "full"
            else "retain-on-failure"
            if should_capture_trace(settings.browser_evidence_mode, collect_all_requested)
            else "off"
        )


def _reduce_allure_fixture_noise(config: pytest.Config) -> None:
    listener = config.pluginmanager.get_plugin("allure_listener")
    if listener is None or getattr(listener, "_biobeat_fixture_filter_installed", False):
        return

    def filtered_fixture_setup(self, fixturedef, request):
        fixture_name = getattr(fixturedef.func, "__allure_display_name__", fixturedef.argname)
        if fixturedef.argname not in ALLURE_REPORTED_FIXTURES:
            yield
            return

        container_uuid = self._cache.get(fixturedef)
        if not container_uuid:
            container_uuid = self._cache.push(fixturedef)
            container = TestResultContainer(uuid=container_uuid)
            self.allure_logger.start_group(container_uuid, container)

        self.allure_logger.update_group(container_uuid, start=now())

        before_fixture_uuid = uuid4()
        before_fixture = TestBeforeResult(name=fixture_name, start=now())
        self.allure_logger.start_before_fixture(container_uuid, before_fixture_uuid, before_fixture)

        outcome = yield

        self.allure_logger.stop_before_fixture(
            before_fixture_uuid,
            stop=now(),
            status=get_outcome_status(outcome),
            statusDetails=get_outcome_status_details(outcome),
        )

        finalizers = getattr(fixturedef, "_finalizers", [])
        for index, finalizer in enumerate(finalizers):
            finalizer_name = getattr(finalizer, "__name__", index)
            name = f"{fixture_name}::{finalizer_name}"
            finalizers[index] = allure_commons.fixture(finalizer, parent_uuid=container_uuid, name=name)

    def filtered_fixture_post_finalizer(self, fixturedef):
        yield
        if fixturedef.argname not in ALLURE_REPORTED_FIXTURES:
            return
        if hasattr(fixturedef, "cached_result") and self._cache.get(fixturedef):
            container_uuid = self._cache.pop(fixturedef)
            self.allure_logger.stop_group(container_uuid, stop=now())

    config.pluginmanager.unregister(name="allure_listener")
    common_name = allure_commons.plugin_manager.get_name(listener)
    if common_name:
        allure_commons.plugin_manager.unregister(name=common_name)

    listener.pytest_fixture_setup = MethodType(filtered_fixture_setup, listener)
    listener.pytest_fixture_post_finalizer = MethodType(filtered_fixture_post_finalizer, listener)
    listener._biobeat_fixture_filter_installed = True

    config.pluginmanager.register(listener, "allure_listener")
    allure_commons.plugin_manager.register(listener, name=common_name or "allure_listener")


def pytest_configure(config: pytest.Config) -> None:
    _runtime(config)
    _reduce_allure_fixture_noise(config)


@pytest.fixture(scope="session", autouse=True)
def write_environment_metadata(settings: Settings) -> None:
    write_allure_environment(
        settings.allure_results_dir,
        {
            "base_url": settings.web_base_url,
            "browser": settings.browser_name,
            "browser_evidence_mode": settings.browser_evidence_mode,
            "environment": settings.runtime.environment.value,
            "headless": str(settings.headless).lower(),
        },
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    _apply_playwright_defaults(config, items)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    runtime = _runtime(session.config)
    runtime.session_context.metadata["exitstatus"] = exitstatus
    runtime.hooks.emit("after_session", runtime.session_context)


def pytest_runtest_setup(item: pytest.Item) -> None:
    runtime = _runtime(item.config)
    context = TestContext(test_id=TestId(item.nodeid), nodeid=item.nodeid, name=item.name, phase="setup")
    item._framework_test_context = context
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
def settings(framework: FrameworkRuntime) -> Settings:
    return framework.settings


@pytest.fixture(scope="session")
def page_factory(framework: FrameworkRuntime, settings: Settings) -> PageObjectFactory:
    return PageObjectFactory(settings=settings, runtime=framework)


@pytest.fixture
def browser_context_args(browser_context_args, settings: Settings):
    return {
        **browser_context_args,
        "ignore_https_errors": settings.browser.ignore_https_errors,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings: Settings):
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": settings.slow_mo_ms,
    }


@pytest.fixture(autouse=True)
def register_playwright_output_path(request, output_path):
    request.node.playwright_output_path = output_path
    return output_path


@pytest.fixture(autouse=True)
def attach_ui_artifacts(request, settings: Settings):
    yield

    report = getattr(request.node, "rep_call", None)
    test_failed = bool(report and report.failed)
    collect_all_evidence = bool(request.node.get_closest_marker("collect_all_evidence"))
    should_collect = should_attach_test_evidence(
        settings.browser_evidence_mode,
        collect_all_evidence,
        test_failed,
    )
    if not should_collect:
        return

    page = request.node.funcargs.get("page")
    with allure.step("Attach UI artifacts"):
        if isinstance(page, Page):
            screenshot_path = settings.screenshots_dir / f"{request.node.name}.png"
            try:
                attach_page_screenshot(page, screenshot_path, test_failed=test_failed)
            except Exception:
                pass

        output_path = getattr(request.node, "playwright_output_path", None)
        if output_path:
            attach_artifacts_from_output_path(output_path)

        attach_log_file(settings.log_dir / "framework.log")
