import allure
from playwright.sync_api import Page

from config.settings import Settings
from ui.pages.base_page import BasePage


class ScansPage(BasePage):
    def __init__(self, page: Page, settings: Settings, *, runtime=None) -> None:
        super().__init__(page, settings, runtime=runtime)
        self.start_scan_button = page.get_by_role("button", name="Start new scan")

    def open(self) -> None:
        self.goto("/scans")
        self.expect_visible(self.page.get_by_test_id("scans-page"), "scans page is visible")

    def start_scan(self) -> None:
        with allure.step("Start scan from UI"):
            self.click(self.start_scan_button, "start new scan button")
