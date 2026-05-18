"""Base class for Playwright page objects."""

import re
from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page, expect

from config.settings import Settings
from ui.actions.playwright_actions import PlaywrightActions

if TYPE_CHECKING:
    from core.framework.runtime import FrameworkRuntime


class BasePage(PlaywrightActions):
    """Base page object with navigation helpers."""

    def __init__(self, page: Page, settings: Settings, *, runtime: FrameworkRuntime | None = None) -> None:
        super().__init__(page, runtime=runtime)
        self.page = page
        self.settings = settings

    def goto(self, path: str) -> None:
        with allure.step(f"Open {path}"):
            self.page.goto(f"{self.settings.web_base_url.rstrip('/')}/{path.lstrip('/')}")

    def expect_path(self, path: str) -> None:
        expect(self.page).to_have_url(re.compile(f".*{re.escape(path)}$"))
