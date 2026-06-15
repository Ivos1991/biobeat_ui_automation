from __future__ import annotations

from playwright.sync_api import Locator

from test_data.patient_admission_cases import PatientAdmissionData
from ui.pages.base_page import BasePage
from ui.pages.patient_admission.exit_patient_admission_popup import ExitPatientAdmissionPopup
from ui.pages.patient_admission.patient_admission_confirmation_popup import PatientAdmissionConfirmationPopup


class PatientAdmissionPage(BasePage):
    """Page object for the BioBeat Patient Admission form."""

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

    def wait_until_ready(self) -> None:
        self.wait_for_loading_to_finish()
        self.patient_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.device_id_input.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)
        self.confirm_button.wait_for(state="visible", timeout=self.settings.timeouts.expect_timeout_ms)

    def fill_patient_id(self, value: str) -> None:
        self.patient_id_input.fill(value)

    def fill_device_id(self, value: str) -> None:
        self.device_id_input.fill(value)

    def fill_first_name(self, value: str) -> None:
        self.first_name_input.fill(value)

    def fill_last_name(self, value: str) -> None:
        self.last_name_input.fill(value)

    def fill_date_of_birth(self, value: str) -> None:
        self.date_of_birth_input.fill(value)

    def fill_weight(self, value: str) -> None:
        self.weight_input.fill(value)

    def fill_height(self, value: str) -> None:
        self.height_input.fill(value)

    def fill_additional_notes(self, value: str) -> None:
        self.additional_notes_input.fill(value)

    def enable_report_completion_emails(self) -> None:
        self.report_completion_emails_checkbox.check(force=True)

    def select_gender_at_birth(self, value: str) -> None:
        normalized = value.strip().lower()
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
        self.referring_physician_combobox.click()
        self.page.get_by_role("option", name=physician_name).click()

    def fill_required_fields(self, patient_id: str | None, device_id: str | None) -> None:
        if patient_id is not None:
            self.fill_patient_id(patient_id)
        if device_id is not None:
            self.fill_device_id(device_id)

    def fill_optional_fields(self, data: PatientAdmissionData) -> None:
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
        self.fill_required_fields(data.patient_id, data.device_id)
        self.fill_optional_fields(data)

    def click_confirm(self) -> None:
        self.confirm_button.click()
        self.wait_for_loading_to_finish()

    def submit_for_confirmation(self) -> PatientAdmissionConfirmationPopup:
        self.click_confirm()
        popup = PatientAdmissionConfirmationPopup(self.page, self.settings, runtime=self.runtime)
        popup.wait_until_open()
        return popup

    def open_exit_popup(self) -> ExitPatientAdmissionPopup:
        self.close_button.click()
        self.wait_for_loading_to_finish()
        popup = ExitPatientAdmissionPopup(self.page, self.settings, runtime=self.runtime)
        popup.wait_until_open()
        return popup

    def get_validation_message(self, message: str) -> Locator:
        return self.page.get_by_text(message)
