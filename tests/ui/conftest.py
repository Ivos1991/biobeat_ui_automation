"""UI-specific fixtures and Playwright artifact handling."""

import pytest
from assertpy import assert_that
from playwright.sync_api import Page

from core.testing_utils.playwright_artifacts import attach_artifacts_from_output_path, attach_page_screenshot
from ui.pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def managed_ui_environment(admin_service, logger):
    logger.info("Reset UI environment before test")
    admin_service.reset_environment()
    yield
    logger.info("Reset UI environment after test")
    admin_service.reset_environment()


@pytest.fixture
def browser_context_args(browser_context_args, settings):
    return {
        **browser_context_args,
        "ignore_https_errors": settings.browser.ignore_https_errors,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings):
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": settings.slow_mo_ms,
    }


@pytest.fixture
def authenticated_page(page: Page, page_factory, settings) -> Page:
    login_page = page_factory.create(LoginPage, page)
    login_page.open()
    login_page.login(settings.username, settings.password)
    assert_that(page.url).described_as("authenticated page URL").contains("/policies")
    return page


@pytest.fixture(autouse=True)
def attach_ui_artifacts_on_failure(request, settings):
    yield

    report = getattr(request.node, "rep_call", None)
    collect_all_evidence = bool(request.node.get_closest_marker("collect_all_evidence"))
    always_collect = settings.browser_evidence_mode == "full_evidence" or collect_all_evidence
    if not report or (not report.failed and not always_collect):
        return
    if request.config.getoption("--screenshot") in ["on", "only-on-failure"]:
        return

    page = request.node.funcargs.get("page")
    if not isinstance(page, Page):
        return

    try:
        attach_page_screenshot(page, settings.artifact_dir / "screenshots" / f"{request.node.name}.png")
    except Exception:
        return


@pytest.fixture(autouse=True)
def register_playwright_output_path(request, output_path):
    request.node.playwright_output_path = output_path
    return output_path


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    output_path = getattr(item, "playwright_output_path", None)
    report = getattr(item, "rep_call", None)
    should_attach = (
        bool(item.get_closest_marker("collect_all_evidence"))
        or bool(report and report.failed)
        or item.config.getoption("--video") == "on"
        or item.config.getoption("--tracing") == "on"
        or item.config.getoption("--screenshot") == "on"
    )

    if not should_attach or not output_path:
        return

    attach_artifacts_from_output_path(output_path)
