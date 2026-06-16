from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class PatientLookupPage(BasePage):
    """Page object for Patient Lookup."""

    # Locator properties expose the search control and the patient result grid.
    @property
    def search_patient_input(self) -> Locator:
        return self.page.locator("#search-patient-input")

    @property
    def patient_table(self) -> Locator:
        return self.page.locator("table")

    @property
    def patient_rows(self) -> Locator:
        return self.page.locator("tbody tr")

    @property
    def create_session_action(self) -> Locator:
        return self.page.locator("[aria-label='Create a new session for this patient']")

    def wait_until_ready(self) -> None:
        """Wait until the lookup search field and results table are ready."""
        self.wait_for_loading_to_finish()
        self.search_patient_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.patient_table.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def search_patient(self, patient_id: str) -> None:
        """Search the patient grid by patient ID and wait for the async filter to finish."""
        self.search_patient_input.fill(patient_id)
        self.wait_for_loading_to_finish(settle_ms=1000)
        self.page.wait_for_timeout(1000)
