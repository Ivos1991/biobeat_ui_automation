import allure
from playwright.sync_api import Locator, expect

from ui.pages.base_page import BasePage
from ui.pages.session_management.remove_session_popup import RemoveSessionPopup


class SessionManagementPage(BasePage):
    """Page object for Session Management."""

    # Locator properties expose the table, search, and row-action entry points used by tests.
    @property
    def search_session_input(self) -> Locator:
        return self.page.locator("#search-session-input")

    @property
    def filter_by_status_button(self) -> Locator:
        return self.page.get_by_text("Filter by Status")

    @property
    def show_hide_columns_button(self) -> Locator:
        return self.page.get_by_text("Show/Hide Columns")

    @property
    def refresh_button(self) -> Locator:
        return self.page.get_by_role("button", name="Refresh Data")

    @property
    def sessions_table(self) -> Locator:
        return self.page.locator("table")

    @property
    def session_rows(self) -> Locator:
        return self.page.locator("tbody tr")

    @property
    def no_sessions_text(self) -> Locator:
        return self.page.get_by_text("No sessions to display")

    def wait_until_ready(self) -> None:
        """Wait until the management table can be queried and refreshed safely."""
        with allure.step("Wait for the Session Management page to become ready"):
            self.wait_for_loading_to_finish()
            self.search_session_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.refresh_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def search_session(self, search_value: str) -> None:
        """Filter the live session table by patient ID or other searchable values."""
        with allure.step(f"Search Session Management for '{search_value}'"):
            self.search_session_input.fill(search_value)
            expect(self.search_session_input).to_have_value(
                search_value,
                timeout=self.settings.timeouts.expect_timeout_ms,
            )
            self.wait_for_loading_to_finish()
            self.sessions_table.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def click_refresh(self) -> None:
        """Trigger a table refresh and wait for the async reload to settle."""
        with allure.step("Refresh the Session Management table"):
            self.refresh_button.click()
        self.wait_for_loading_to_finish()
        self.refresh_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def find_row_by_patient_id(self, patient_id: str) -> Locator | None:
        """Return the first non-empty session row that contains the requested patient ID."""
        rows = self.session_rows
        for index in range(rows.count()):
            row = rows.nth(index)
            row_text = row.inner_text().strip()
            if not row_text or "No sessions to display" in row_text:
                continue
            if patient_id in row_text:
                return row
        return None

    def has_session(self, patient_id: str) -> bool:
        """Tell tests whether a session row for the patient is currently visible."""
        with allure.step(f"Check whether session '{patient_id}' is visible"):
            return self.find_row_by_patient_id(patient_id) is not None

    def get_row_text(self, patient_id: str) -> str:
        """Return the raw row text so tests can assert patient, device, and status in one read."""
        with allure.step(f"Read the Session Management row text for '{patient_id}'"):
            row = self.find_row_by_patient_id(patient_id)
            return row.inner_text() if row is not None else ""

    def open_row_actions(self, patient_id: str) -> bool:
        """Open the row action menu for a given patient when a matching session exists."""
        with allure.step(f"Open the row actions menu for session '{patient_id}'"):
            row = self.find_row_by_patient_id(patient_id)
            if row is None:
                return False
            action_button = row.locator("button").first
            row.hover()
            action_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            action_button.click()
            return True

    def open_remove_session_popup(self, patient_id: str) -> RemoveSessionPopup | None:
        """Open the Remove Session popup for a visible session row and return its page object."""
        with allure.step(f"Open the Remove Session popup for '{patient_id}'"):
            if not self.open_row_actions(patient_id):
                return None
            self.page.get_by_role("menuitem", name="Remove Session").click()
            popup = RemoveSessionPopup(self.page, self.settings, runtime=self.runtime)
            popup.wait_until_open()
            return popup
