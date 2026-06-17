import allure
from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class AppShellPage(BasePage):
    """Authenticated shell navigation helpers."""

    # Locator properties expose the verified left-menu entries shared across screens.
    @property
    def session_management_button(self) -> Locator:
        return self.page.locator("#session-management-button")

    @property
    def patient_admission_button(self) -> Locator:
        return self.page.locator("#patient-admission-button")

    @property
    def patient_lookup_button(self) -> Locator:
        return self.page.locator("#patient-lookup-button")

    def wait_until_ready(self) -> None:
        """Wait for the authenticated shell to be usable after login or route changes."""
        with allure.step("Wait for the authenticated shell navigation to become ready"):
            self.session_management_button.wait_for(
                state="visible",
                timeout=self.settings.timeouts.navigation_timeout_ms * 2,
            )
        self.wait_for_loading_to_finish()

    def open_session_management(self) -> None:
        """Navigate through the shell to Session Management."""
        with allure.step("Click the Session Management navigation button"):
            self.session_management_button.click()
        self.wait_for_path("/session-management")
        self.wait_for_loading_to_finish()

    def open_patient_admission(self) -> None:
        """Navigate through the shell to Patient Admission."""
        with allure.step("Click the Patient Admission navigation button"):
            self.patient_admission_button.click()
        self.wait_for_path("/patient-admission")
        self.wait_for_loading_to_finish()

    def open_patient_lookup(self) -> None:
        """Navigate through the shell to Patient Lookup."""
        with allure.step("Click the Patient Lookup navigation button"):
            self.patient_lookup_button.click()
        self.wait_for_path("/patient-lookup")
        self.wait_for_loading_to_finish()
