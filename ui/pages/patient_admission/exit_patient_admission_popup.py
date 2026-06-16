from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class ExitPatientAdmissionPopup(BasePage):
    """Page object for the dirty-form exit confirmation popup."""

    # Locator properties expose the popup title and the two navigation decisions.
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
        """Wait until the exit confirmation popup is visible."""
        self.title.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def click_cancel(self) -> None:
        """Stay on the admission form and discard the popup only."""
        self.cancel_button.click()
        self.wait_for_loading_to_finish()

    def click_leave(self) -> None:
        """Leave the dirty admission form and return to the previous screen."""
        self.leave_button.click()
        self.wait_for_loading_to_finish()
