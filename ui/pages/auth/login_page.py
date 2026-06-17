import allure
from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the public BioBeat login screen."""

    # Locator properties expose the verified controls used by the login smoke path.
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
        """Navigate directly to the configured login route."""
        self.goto(self.settings.login_path)

    def wait_until_ready(self) -> None:
        """Wait until the login form is ready for interaction."""
        with allure.step("Wait for the login form to become ready"):
            self.email_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.password_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.login_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_email(self, value: str) -> None:
        """Type the username or email into the login form."""
        with allure.step(f"Fill the email field with '{value}'"):
            self.email_input.fill(value)

    def fill_password(self, value: str) -> None:
        """Type the password into the login form."""
        with allure.step("Fill the password field"):
            self.password_input.fill(value)

    def click_login(self) -> None:
        """Submit the login form and wait for the next screen to load."""
        with allure.step("Click the Login button"):
            self.login_button.click()
        self.wait_for_loading_to_finish()

    def login(self, username: str, password: str) -> None:
        """Perform the complete login interaction used by smoke and navigation tests."""
        with allure.step("Complete the login form and submit it"):
            self.fill_email(username)
            self.fill_password(password)
            self.click_login()
