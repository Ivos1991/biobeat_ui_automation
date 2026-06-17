import allure
import pytest

from flows.admission_flow import PatientAdmissionFlow
from test_data.patient_admission_cases import build_complete_admission, build_happy_path_admission
from utils.assertions import assert_that


@pytest.mark.ui
def test_confirmation_popup_enablement_expects_exact_patient_id_before_confirm(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the admission confirmation popup enables only for the exact patient ID."""
    data = build_happy_path_admission()

    with allure.step("Open the admission confirmation popup with valid form data"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        popup = ready_admission_flow.patient_admission_page.submit_for_confirmation()

    with allure.step("Verify the popup confirm button stays disabled for empty and wrong values"):
        assert_that(
            popup.confirm_button,
            "Popup confirm button should start disabled",
        ).is_disabled()
        popup.fill_patient_id("wrong-value")
        assert_that(
            popup.confirm_button,
            "Popup confirm button should remain disabled for the wrong patient ID",
        ).is_disabled()
        popup.fill_patient_id("")
        assert_that(
            popup.confirm_button,
            "Popup confirm button should remain disabled for an empty patient ID",
        ).is_disabled()

    with allure.step("Verify the popup confirm button enables for the exact patient ID"):
        popup.fill_patient_id(data.patient_id)
        assert_that(
            popup.confirm_button,
            "Popup confirm button should enable for the exact patient ID",
        ).is_enabled()
        popup.click_cancel()

    with allure.step("Verify the user remains on Patient Admission after cancelling the popup"):
        assert_that(
            ready_admission_flow.patient_admission_page.patient_id_input.input_value(),
            "Patient ID should remain filled after cancelling the confirmation popup",
        ).is_equal_to(data.patient_id)


@pytest.mark.ui
def test_exit_popup_behavior_expects_cancel_to_keep_form_and_leave_to_exit(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the exit popup preserves draft data on cancel and leaves on explicit confirmation."""
    data = build_happy_path_admission()

    with allure.step("Enter Patient ID to create a dirty admission form"):
        ready_admission_flow.patient_admission_page.fill_patient_id(data.patient_id)

    with allure.step("Open the exit popup and cancel it"):
        exit_popup = ready_admission_flow.patient_admission_page.open_exit_popup()
        exit_popup.click_cancel()

    with allure.step("Verify the form keeps the typed Patient ID after cancelling exit"):
        assert_that(
            ready_admission_flow.patient_admission_page.patient_id_input.input_value(),
            "Patient ID should remain after cancelling the exit popup",
        ).is_equal_to(data.patient_id)

    with allure.step("Open the exit popup again and leave the page"):
        exit_popup = ready_admission_flow.patient_admission_page.open_exit_popup()
        exit_popup.click_leave()
        ready_admission_flow.session_management_page.wait_until_ready()

    with allure.step("Verify the user returns to Session Management after leaving"):
        assert_that(
            ready_admission_flow.session_management_page.search_session_input,
            "Session search input should be visible after leaving Patient Admission",
        ).is_visible()
        assert_that(
            ready_admission_flow.session_management_page.current_url,
            "Leaving Patient Admission should return the user to Session Management",
        ).contains("/session-management")


@pytest.mark.ui
def test_female_gender_selection_expects_confirmation_popup_to_open(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the Female gender option is accepted as part of an otherwise valid submission."""
    data = build_complete_admission(device_id="989898", gender_at_birth="Female")

    with allure.step("Submit the form with Female selected as Gender at birth"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        popup = ready_admission_flow.patient_admission_page.submit_for_confirmation()

    with allure.step("Verify the confirmation popup opens with the submitted Patient ID"):
        assert_that(
            popup.patient_id_input,
            "The confirmation popup Patient ID input should be visible",
        ).is_visible()
        popup.click_cancel()
