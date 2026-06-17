import allure
from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class RemoveSessionPopup(BasePage):
    """Page object for the session-removal confirmation popup."""

    # Locator properties expose the confirmation input and the destructive action buttons.
    @property
    def title(self) -> Locator:
        return self.page.get_by_role("heading", name="Remove Session")

    @property
    def patient_id_confirmation_input(self) -> Locator:
        return self.page.get_by_label("Enter Patient ID")

    @property
    def cancel_button(self) -> Locator:
        return self.page.get_by_role("button", name="Cancel")

    @property
    def remove_button(self) -> Locator:
        return self.page.get_by_role("button", name="Remove")

    def wait_until_open(self) -> None:
        """Wait until the remove-session popup is visible and ready for confirmation input."""
        with allure.step("Wait for the Remove Session popup to open"):
            self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.patient_id_confirmation_input.wait_for(
                state="visible",
                timeout=self.settings.timeouts.expect_timeout_ms,
            )

    def fill_patient_id_confirmation(self, patient_id: str) -> None:
        """Type the exact patient ID required by the live app to enable removal."""
        with allure.step(f"Fill the Remove Session confirmation input with '{patient_id}'"):
            self.patient_id_confirmation_input.fill(patient_id)

    def click_cancel(self) -> None:
        """Close the popup without deleting the session."""
        with allure.step("Click Cancel in the Remove Session popup"):
            self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_remove(self) -> None:
        """Confirm deletion once the patient-ID safeguard has been satisfied."""
        with allure.step("Click Remove in the Remove Session popup"):
            self.remove_button.click()
        self.wait_for_loading_to_finish()
