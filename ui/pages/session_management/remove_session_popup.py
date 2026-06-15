from __future__ import annotations

from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class RemoveSessionPopup(BasePage):
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
        self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.patient_id_confirmation_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_patient_id_confirmation(self, patient_id: str) -> None:
        self.patient_id_confirmation_input.fill(patient_id)

    def click_cancel(self) -> None:
        self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_remove(self) -> None:
        self.remove_button.click()
        self.wait_for_loading_to_finish(settle_ms=1200)
