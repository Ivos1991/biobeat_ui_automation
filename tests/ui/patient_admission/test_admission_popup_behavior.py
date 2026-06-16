import allure
import pytest

from test_data.patient_admission_cases import build_happy_path_admission
from utils.assertions import assert_that


@pytest.mark.ui
def test_confirmation_popup_enablement_expects_exact_patient_id_before_confirm(admission_flow) -> None:
    """Verify the admission confirmation popup enables only for the exact patient ID."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Open the admission confirmation popup with valid form data"):
        admission_flow.patient_admission_page.fill_form(data)
        popup = admission_flow.patient_admission_page.submit_for_confirmation()

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
            admission_flow.patient_admission_page.patient_id_input.input_value(),
            "Patient ID should remain filled after cancelling the confirmation popup",
        ).is_equal_to(data.patient_id)


@pytest.mark.ui
def test_exit_popup_behavior_expects_cancel_to_keep_form_and_leave_to_exit(admission_flow) -> None:
    """Verify the exit popup preserves draft data on cancel and leaves on explicit confirmation."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Enter Patient ID to create a dirty admission form"):
        admission_flow.patient_admission_page.fill_patient_id(data.patient_id)

    with allure.step("Open the exit popup and cancel it"):
        exit_popup = admission_flow.patient_admission_page.open_exit_popup()
        exit_popup.click_cancel()

    with allure.step("Verify the form keeps the typed Patient ID after cancelling exit"):
        assert_that(
            admission_flow.patient_admission_page.patient_id_input.input_value(),
            "Patient ID should remain after cancelling the exit popup",
        ).is_equal_to(data.patient_id)

    with allure.step("Open the exit popup again and leave the page"):
        exit_popup = admission_flow.patient_admission_page.open_exit_popup()
        exit_popup.click_leave()
        admission_flow.session_management_page.wait_until_ready()

    with allure.step("Verify the user returns to Session Management after leaving"):
        assert_that(
            admission_flow.session_management_page.search_session_input,
            "Session search input should be visible after leaving Patient Admission",
        ).is_visible()
        assert_that(
            admission_flow.session_management_page.current_url,
            "Leaving Patient Admission should return the user to Session Management",
        ).contains("/session-management")
