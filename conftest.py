"""Global pytest configuration and framework bootstrap."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Page

from config.settings import Settings
from core.framework.hooks import FailureContext, TestContext
from core.framework.runtime import FrameworkRuntime, build_runtime
from core.framework.types import TestId
from core.testing_utils.playwright_artifacts import (
    attach_artifacts_from_output_path,
    attach_log_file,
    attach_page_screenshot,
)
from ui.page_factory import PageObjectFactory


def _runtime(config: pytest.Config) -> FrameworkRuntime:
    runtime = getattr(config, "_framework_runtime", None)
    if runtime is None:
        runtime = build_runtime()
        config._framework_runtime = runtime
    return runtime


def _apply_playwright_defaults(config: pytest.Config, items: list[pytest.Item]) -> None:
    runtime = _runtime(config)
    settings = runtime.settings
    force_always = settings.browser_evidence_mode == "full_evidence" or any(
        item.get_closest_marker("collect_all_evidence") for item in items
    )

    if getattr(config.option, "browser", None) in (None, []):
        config.option.browser = [settings.browser_name]

    if getattr(config.option, "output", None) == "test-results":
        config.option.output = str(Path(settings.artifact_dir) / "playwright")

    if settings.browser_evidence_mode == "off":
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
    collect_all_evidence = bool(request.node.get_closest_marker("collect_all_evidence"))
    always_collect = settings.browser_evidence_mode == "full_evidence" or collect_all_evidence
    should_collect = bool(report and report.failed) or always_collect
    if not should_collect:
        return

    page = request.node.funcargs.get("page")
    if isinstance(page, Page):
        screenshot_path = settings.artifact_dir / "screenshots" / f"{request.node.name}.png"
        try:
            attach_page_screenshot(page, screenshot_path)
        except Exception:
            pass

    output_path = getattr(request.node, "playwright_output_path", None)
    if output_path:
        attach_artifacts_from_output_path(output_path)

    attach_log_file(settings.log_dir / "framework.log")
