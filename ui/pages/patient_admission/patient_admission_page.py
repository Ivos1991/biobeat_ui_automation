import allure
from playwright.sync_api import Locator

from test_data.patient_admission_cases import PatientAdmissionData
from ui.pages.base_page import BasePage
from ui.pages.patient_admission.exit_patient_admission_popup import ExitPatientAdmissionPopup
from ui.pages.patient_admission.patient_admission_confirmation_popup import PatientAdmissionConfirmationPopup


class PatientAdmissionPage(BasePage):
    """Page object for the BioBeat Patient Admission form."""

    # Locator properties expose the verified form controls and action buttons.
    @property
    def patient_id_input(self) -> Locator:
        return self.page.locator("input[name='patient_id']")

    @property
    def device_id_input(self) -> Locator:
        return self.page.locator("input[name='device_id']")

    @property
    def first_name_input(self) -> Locator:
        return self.page.locator("input[name='first_name']")

    @property
    def last_name_input(self) -> Locator:
        return self.page.locator("input[name='last_name']")

    @property
    def male_gender_radio(self) -> Locator:
        return self.page.locator("input[value='male']")

    @property
    def female_gender_radio(self) -> Locator:
        return self.page.locator("input[value='female']")

    @property
    def date_of_birth_input(self) -> Locator:
        return self.page.locator("input[name='dob']")

    @property
    def weight_input(self) -> Locator:
        return self.page.locator("input[name='weight']")

    @property
    def height_input(self) -> Locator:
        return self.page.locator("input[name='height']")

    @property
    def referring_physician_combobox(self) -> Locator:
        return self.page.get_by_role("combobox")

    @property
    def additional_notes_input(self) -> Locator:
        return self.page.locator("textarea[name='notes']")

    @property
    def report_completion_emails_checkbox(self) -> Locator:
        return self.page.locator("input[name='report_email']")

    @property
    def confirm_button(self) -> Locator:
        return self.page.get_by_role("button", name="Confirm").first

    @property
    def close_button(self) -> Locator:
        return self.page.locator("button:has(svg[data-testid='CloseIcon'])")

    @property
    def success_feedback(self) -> Locator:
        return self.page.get_by_text("added successfully")

    @property
    def generic_form_error(self) -> Locator:
        return self.page.get_by_text("Please correct form errors")

    def wait_until_ready(self) -> None:
        """Wait for the admission form and its primary required controls to become usable."""
        with allure.step("Wait for the Patient Admission form to become ready"):
            self.wait_for_loading_to_finish()
            self.patient_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.device_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
            self.confirm_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_patient_id(self, value: str) -> None:
        """Enter the department-scoped patient identifier."""
        with allure.step(f"Fill Patient ID with '{value}'"):
            self.patient_id_input.fill(value)

    def fill_device_id(self, value: str) -> None:
        """Enter the device identifier that will be validated by the live application."""
        with allure.step(f"Fill Device ID with '{value}'"):
            self.device_id_input.fill(value)

    def fill_first_name(self, value: str) -> None:
        """Enter the patient first name."""
        with allure.step(f"Fill First Name with '{value}'"):
            self.first_name_input.fill(value)

    def fill_last_name(self, value: str) -> None:
        """Enter the patient last name."""
        with allure.step(f"Fill Last Name with '{value}'"):
            self.last_name_input.fill(value)

    def fill_date_of_birth(self, value: str) -> None:
        """Enter the date of birth using the UI input format expected by the app."""
        with allure.step(f"Fill Date of Birth with '{value}'"):
            self.date_of_birth_input.fill(value)

    def fill_weight(self, value: str) -> None:
        """Enter the patient weight for validation scenarios or happy-path submissions."""
        with allure.step(f"Fill Weight with '{value}'"):
            self.weight_input.fill(value)

    def fill_height(self, value: str) -> None:
        """Enter the patient height for validation scenarios or happy-path submissions."""
        with allure.step(f"Fill Height with '{value}'"):
            self.height_input.fill(value)

    def fill_additional_notes(self, value: str) -> None:
        """Enter free-text notes into the optional notes field."""
        with allure.step(f"Fill Additional Notes with '{value}'"):
            self.additional_notes_input.fill(value)

    def enable_report_completion_emails(self) -> None:
        """Enable the optional report completion email checkbox when a test needs it."""
        with allure.step("Enable report completion emails"):
            self.report_completion_emails_checkbox.check(force=True)

    def select_gender_at_birth(self, value: str) -> None:
        """Select one of the supported gender-at-birth options exposed by the UI."""
        normalized = value.strip().lower()
        with allure.step(f"Select Gender at birth as '{value}'"):
            if normalized == "male":
                if not self.male_gender_radio.is_checked():
                    self.page.locator("label").filter(has_text="Male").first.click()
                return
            if normalized == "female":
                if not self.female_gender_radio.is_checked():
                    self.page.locator("label").filter(has_text="Female").first.click()
                return
            raise ValueError(f"Unsupported gender value: {value}")

    def select_referring_physician(self, physician_name: str) -> None:
        """Open the physician combo box and choose the requested live option."""
        with allure.step(f"Select Referring Physician '{physician_name}'"):
            self.referring_physician_combobox.click()
            self.page.get_by_role("option", name=physician_name).click()

    def fill_required_fields(self, patient_id: str | None, device_id: str | None) -> None:
        """Populate only the required fields so negative tests can omit one side intentionally."""
        with allure.step("Populate the required Patient Admission fields"):
            if patient_id is not None:
                self.fill_patient_id(patient_id)
            if device_id is not None:
                self.fill_device_id(device_id)

    def fill_optional_fields(self, data: PatientAdmissionData) -> None:
        """Populate whichever optional fields are present in the supplied data object."""
        with allure.step("Populate the optional Patient Admission fields that are present"):
            if data.gender_at_birth:
                self.select_gender_at_birth(data.gender_at_birth)
            if data.referring_physician:
                self.select_referring_physician(data.referring_physician)
            if data.first_name:
                self.fill_first_name(data.first_name)
            if data.last_name:
                self.fill_last_name(data.last_name)
            if data.date_of_birth:
                self.fill_date_of_birth(data.date_of_birth)
            if data.weight:
                self.fill_weight(data.weight)
            if data.height:
                self.fill_height(data.height)
            if data.additional_notes:
                self.fill_additional_notes(data.additional_notes)
            if data.receive_report_completion_emails:
                self.enable_report_completion_emails()

    def fill_form(self, data: PatientAdmissionData) -> None:
        """Fill the complete admission form from the shared test-data model."""
        with allure.step("Populate the Patient Admission form from the shared test data"):
            self.fill_required_fields(data.patient_id, data.device_id)
            self.fill_optional_fields(data)

    def click_confirm(self) -> None:
        """Click the form-level Confirm button and wait for the next UI state to settle."""
        with allure.step("Click the Patient Admission Confirm button"):
            self.confirm_button.click()
        self.wait_for_loading_to_finish()

    def submit_for_confirmation(self) -> PatientAdmissionConfirmationPopup:
        """Submit the form and return the confirmation popup used to finalize admission."""
        with allure.step("Submit the Patient Admission form and open the confirmation popup"):
            self.click_confirm()
            popup = PatientAdmissionConfirmationPopup(self.page, self.settings, runtime=self.runtime)
            popup.wait_until_open()
            return popup

    def open_exit_popup(self) -> ExitPatientAdmissionPopup:
        """Open the leave-page confirmation popup from the close icon."""
        with allure.step("Open the exit confirmation popup from Patient Admission"):
            self.close_button.click()
            self.wait_for_loading_to_finish()
            popup = ExitPatientAdmissionPopup(self.page, self.settings, runtime=self.runtime)
            popup.wait_until_open()
            return popup

    def get_validation_message(self, message: str) -> Locator:
        """Return a locator for a concrete validation message asserted by negative tests."""
        with allure.step(f"Locate the validation message '{message}'"):
            return self.page.get_by_text(message)

    def wait_for_submission_result(self) -> None:
        """Wait for either success feedback or the form to remain on-screen with validation."""
        with allure.step("Wait for admission success, validation feedback, or Session Management redirect"):
            self.page.wait_for_function(
                """
                () => {
                    const text = document.body.innerText || "";
                    return (
                        window.location.pathname.includes("/session-management") ||
                        text.includes("added successfully") ||
                        text.includes("Please correct form errors") ||
                        text.includes("Error admitting this patient") ||
                        text.includes("Device is in use.") ||
                        text.includes("Device is not activated or does not exist.")
                    );
                }
                """,
                timeout=self.settings.timeouts.navigation_timeout_ms * 2,
            )
