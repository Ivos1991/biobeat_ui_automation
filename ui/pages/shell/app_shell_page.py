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
        self.session_management_button.wait_for(
            state="visible",
            timeout=self.settings.timeouts.navigation_timeout_ms * 2,
        )
        self.wait_for_loading_to_finish(settle_ms=1000)

    def open_session_management(self) -> None:
        """Navigate through the shell to Session Management."""
        self.session_management_button.click()
        self.wait_for_url("**/session-management")
        self.wait_for_loading_to_finish()

    def open_patient_admission(self) -> None:
        """Navigate through the shell to Patient Admission."""
        self.patient_admission_button.click()
        self.wait_for_url("**/patient-admission")
        self.wait_for_loading_to_finish()

    def open_patient_lookup(self) -> None:
        """Navigate through the shell to Patient Lookup."""
        self.patient_lookup_button.click()
        self.wait_for_url("**/patient-lookup")
        self.wait_for_loading_to_finish()
