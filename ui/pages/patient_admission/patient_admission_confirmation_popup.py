from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class PatientAdmissionConfirmationPopup(BasePage):
    """Page object for the patient-ID confirmation popup shown before final admission."""

    # Locator properties expose the popup title, input, and action buttons.
    @property
    def title(self) -> Locator:
        return self.page.get_by_text("Please confirm the patient ID to complete the admission process")

    @property
    def patient_id_input(self) -> Locator:
        return self.page.get_by_label("Patient ID").last

    @property
    def cancel_button(self) -> Locator:
        return self.page.get_by_role("button", name="Cancel")

    @property
    def confirm_button(self) -> Locator:
        return self.page.get_by_role("button", name="Confirm").last

    def wait_until_open(self) -> None:
        """Wait until the confirmation popup is visible and ready for input."""
        self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.patient_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_patient_id(self, value: str) -> None:
        """Type the same patient ID used in the main form to unlock final confirmation."""
        self.patient_id_input.fill(value)

    def click_cancel(self) -> None:
        """Dismiss the popup without completing the admission."""
        self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_confirm(self) -> None:
        """Finalize the admission from the popup after the patient ID is confirmed."""
        self.confirm_button.click()
        self.wait_for_loading_to_finish(settle_ms=1000)
