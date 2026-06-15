from __future__ import annotations

from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class ExitPatientAdmissionPopup(BasePage):
    @property
    def title(self) -> Locator:
        return self.page.get_by_text("Exit Patient Admission")

    @property
    def cancel_button(self) -> Locator:
        return self.page.get_by_role("button", name="Cancel")

    @property
    def leave_button(self) -> Locator:
        return self.page.get_by_role("button", name="Leave")

    def wait_until_open(self) -> None:
        self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def click_cancel(self) -> None:
        self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_leave(self) -> None:
        self.leave_button.click()
        self.wait_for_loading_to_finish()
