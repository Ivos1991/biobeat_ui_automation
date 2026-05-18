import allure
from playwright.sync_api import Page

from config.settings import Settings
from ui.pages.alert_details_drawer import AlertDetailsDrawer
from ui.pages.base_page import BasePage


class AlertsPage(BasePage):
    def __init__(self, page: Page, settings: Settings, *, runtime=None) -> None:
        super().__init__(page, settings, runtime=runtime)
        self.search_input = page.get_by_label("Search alerts by policy name, asset location, or description")
        self.table = page.locator("table[aria-label='Alerts list']")
        self.drawer = AlertDetailsDrawer(page, settings, runtime=runtime)

    def open(self) -> None:
        self.goto("/alerts")
        self.expect_visible(self.page.get_by_test_id("alerts-page"), "alerts page is visible")
        self.expect_visible(self.table, "alerts table is visible")

    def search(self, query: str) -> None:
        with allure.step(f"Search alerts for {query}"):
            self.fill(self.search_input, query, "alert search input")

    def open_alert_by_policy_name(self, policy_name: str) -> None:
        with allure.step(f"Open alert row for {policy_name}"):
            self.search(policy_name)
            row = self.page.locator("table[aria-label='Alerts list'] tbody tr").first
            self.expect_visible(row, f"first alert row after filtering by policy name {policy_name}")
            self.click(row, f"open first alert row after filtering by policy name {policy_name}")
            self.drawer.wait_until_open()
