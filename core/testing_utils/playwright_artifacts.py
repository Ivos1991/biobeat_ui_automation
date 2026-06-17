from pathlib import Path
from typing import Any

import allure
from playwright.sync_api import Page

from core.reporting import attach_file, attach_text


def attachment_type_for_path(path: Path) -> Any:
    """Map a file suffix to the matching Allure attachment type."""
    suffix = path.suffix.lower()
    if suffix == ".png":
        return allure.attachment_type.PNG
    if suffix == ".webm":
        return allure.attachment_type.WEBM
    if suffix == ".zip":
        return allure.attachment_type.ZIP
    return allure.attachment_type.TEXT


def attach_artifacts_from_output_path(output_path: str | Path) -> None:
    """Attach supported Playwright artifacts from the pytest-playwright output folder."""
    artifact_dir = Path(output_path)
    if not artifact_dir.exists():
        return

    files_to_attach = sorted(
        path
        for path in artifact_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".webm", ".zip"}
    )
    for path in files_to_attach:
        attach_file(path.name, path, attachment_type_for_path(path))


def attach_page_screenshot(page: Page, screenshot_path: Path, *, test_failed: bool) -> None:
    """Capture a full-page screenshot and attach it together with the current page URL."""
    if page.is_closed():
        return

    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(screenshot_path), full_page=True)
    attachment_name = "failure-screenshot" if test_failed else "page-screenshot"
    attach_file(attachment_name, screenshot_path, allure.attachment_type.PNG)
    attach_text("page-url", page.url)


def attach_log_file(log_path: Path) -> None:
    """Attach the framework log file when it exists for the current run."""
    if log_path.exists():
        attach_file(log_path.name, log_path, allure.attachment_type.TEXT)
