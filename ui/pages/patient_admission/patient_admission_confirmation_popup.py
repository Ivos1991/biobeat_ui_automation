from __future__ import annotations

from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class PatientAdmissionConfirmationPopup(BasePage):
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
        self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.patient_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_patient_id(self, value: str) -> None:
        self.patient_id_input.fill(value)

    def click_cancel(self) -> None:
        self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_confirm(self) -> None:
        self.confirm_button.click()
        self.wait_for_loading_to_finish(settle_ms=1000)
