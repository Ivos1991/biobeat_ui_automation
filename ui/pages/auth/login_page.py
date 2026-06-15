from __future__ import annotations

from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    @property
    def email_input(self) -> Locator:
        return self.page.get_by_placeholder("Email")

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_placeholder("Password")

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Login")

    def open(self) -> None:
        self.goto(self.settings.login_path)

    def wait_until_ready(self) -> None:
        self.email_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.password_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.login_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_email(self, value: str) -> None:
        self.email_input.fill(value)

    def fill_password(self, value: str) -> None:
        self.password_input.fill(value)

    def click_login(self) -> None:
        self.login_button.click()
        self.wait_for_loading_to_finish()

    def login(self, username: str, password: str) -> None:
        self.fill_email(username)
        self.fill_password(password)
        self.click_login()
