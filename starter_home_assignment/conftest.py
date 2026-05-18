import os
from pathlib import Path

import pytest

from config.settings import Settings
from core.core_utils.logger import configure_logging, get_logger


VALID_BROWSER_EVIDENCE_MODES = {"off", "on_failure", "always"}


def _cli_option_present(config: pytest.Config, option_name: str) -> bool:
    return option_name in config.invocation_params.args


def _browser_evidence_mode() -> str:
    mode = os.getenv("BROWSER_EVIDENCE_MODE", "on_failure").strip().lower()
    if mode not in VALID_BROWSER_EVIDENCE_MODES:
        raise pytest.UsageError(
            "BROWSER_EVIDENCE_MODE must be one of: off, on_failure, always"
        )
    return mode


def _apply_playwright_artifact_defaults(config: pytest.Config, items: list[pytest.Item]) -> None:
    mode = _browser_evidence_mode()
    has_collect_all_marker = any(
        item.get_closest_marker("collect_all_evidence") for item in items
    )
    force_always = mode == "always" or has_collect_all_marker

    if (
        not _cli_option_present(config, "--output")
        and getattr(config.option, "output", None) == "test-results"
    ):
        config.option.output = str(Path(os.getenv("ARTIFACT_DIR", "artifacts")) / "playwright")

    if mode == "off":
        return

    if (
        not _cli_option_present(config, "--screenshot")
        and getattr(config.option, "screenshot", None) == "off"
    ):
        config.option.screenshot = "on" if force_always else "only-on-failure"

    if (
        not _cli_option_present(config, "--video")
        and getattr(config.option, "video", None) == "off"
    ):
        config.option.video = "on" if force_always else "retain-on-failure"

    if (
        not _cli_option_present(config, "--tracing")
        and getattr(config.option, "tracing", None) == "off"
    ):
        config.option.tracing = "on" if force_always else "retain-on-failure"


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    _apply_playwright_artifact_defaults(config, items)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture(scope="session", autouse=True)
def framework_logging(settings: Settings) -> None:
    configure_logging(settings.log_dir, settings.log_level)


@pytest.fixture(scope="session")
def logger():
    return get_logger("tests")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
