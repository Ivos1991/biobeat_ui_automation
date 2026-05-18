import allure
from playwright.sync_api import Page

from config.settings import Settings
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, settings: Settings, *, runtime=None) -> None:
        super().__init__(page, settings, runtime=runtime)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.get_by_role("button", name="Sign in")

    def open(self) -> None:
        self.goto("/login")
        self.expect_visible(self.page.get_by_test_id("login-page"), "login page is visible")

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Login as {username}"):
            self.fill(self.username_input, username, "username field")
            self.fill(self.password_input, password, "password field")
            self.click(self.submit_button, "sign in button")
            self.expect_path("/policies")
