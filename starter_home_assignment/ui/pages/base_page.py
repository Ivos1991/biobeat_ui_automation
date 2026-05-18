import re

import allure
from playwright.sync_api import Page, expect

from config.settings import Settings
from ui.actions.playwright_actions import PlaywrightActions


class BasePage(PlaywrightActions):
    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page)
        self.page = page
        self.settings = settings

    def goto(self, path: str) -> None:
        with allure.step(f"Open {path}"):
            self.page.goto(f"{self.settings.web_base_url.rstrip('/')}/{path.lstrip('/')}")

    def expect_path(self, path: str) -> None:
        expect(self.page).to_have_url(re.compile(f".*{re.escape(path)}$"))
