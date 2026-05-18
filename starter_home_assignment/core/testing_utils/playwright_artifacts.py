from pathlib import Path

import allure
from playwright.sync_api import Page

from core.reporting import attach_file, attach_text


def attachment_type_for_path(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".png":
        return allure.attachment_type.PNG
    if suffix == ".webm":
        return allure.attachment_type.WEBM
    if suffix == ".zip":
        return allure.attachment_type.ZIP
    return allure.attachment_type.TEXT


def attach_artifacts_from_output_path(output_path: str | Path) -> None:
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


def attach_page_screenshot(page: Page, screenshot_path: Path) -> None:
    if page.is_closed():
        return

    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(screenshot_path), full_page=True)
    attach_file("failure-screenshot", screenshot_path, allure.attachment_type.PNG)
    attach_text("page-url", page.url)
