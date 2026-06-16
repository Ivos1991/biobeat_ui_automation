import allure
import pytest

from test_data.patient_admission_cases import PatientAdmissionData, build_happy_path_admission
from tests.ui.patient_admission.support import DEVICE_IN_USE_ID, DEVICE_NOT_ACTIVATED_ID
from utils.assertions import assert_that


@pytest.mark.ui
def test_missing_required_patient_id_expects_validation_feedback(admission_flow) -> None:
    """Verify the form blocks submission when Patient ID is missing."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form without Patient ID"):
        admission_flow.patient_admission_page.fill_required_fields(patient_id=None, device_id=data.device_id)
        admission_flow.patient_admission_page.fill_optional_fields(data)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the Patient ID required validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message("Patient ID is required"),
            "Patient ID required validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_missing_required_device_id_expects_validation_feedback(admission_flow) -> None:
    """Verify the form blocks submission when Device ID is missing."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form without Device ID"):
        admission_flow.patient_admission_page.fill_required_fields(patient_id=data.patient_id, device_id=None)
        admission_flow.patient_admission_page.fill_optional_fields(data)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the Device ID required validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message("Device ID is required"),
            "Device ID required validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_device_shorter_than_minimum_expects_validation_feedback(admission_flow) -> None:
    """Verify the Device ID minimum-length validation using a too-short live input."""
    data = build_happy_path_admission(device_id="9")

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form with a device ID shorter than the minimum length"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the short Device ID validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message("Device ID must be at least 4 characters"),
            "Short Device ID validation should be visible",
        ).is_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    ("device_id", "expected_message"),
    [
        (DEVICE_IN_USE_ID, "Device is in use."),
        (DEVICE_NOT_ACTIVATED_ID, "Device is not activated or does not exist."),
    ],
)
def test_invalid_device_states_expect_distinct_feedback(admission_flow, device_id: str, expected_message: str) -> None:
    """Verify that different invalid live device states map to different UI messages."""
    data = build_happy_path_admission(device_id=device_id)

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step(f"Submit the form with device '{device_id}'"):
        admission_flow.patient_admission_page.fill_form(data)
        popup = admission_flow.patient_admission_page.submit_for_confirmation()
        popup.fill_patient_id(data.patient_id)
        popup.click_confirm()

    with allure.step("Verify the device-state validation message on Patient Admission"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message(expected_message),
            "Device-state validation should be visible after final confirmation",
        ).is_visible()
        assert_that(
            admission_flow.patient_admission_page.current_url,
            "The user should remain on Patient Admission when the device state is invalid",
        ).contains("/patient-admission")


@pytest.mark.ui
def test_invalid_first_name_expects_validation_feedback(admission_flow) -> None:
    """Verify the first-name field rejects numeric input."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form with an invalid first name"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.fill_first_name("123")
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the invalid first-name validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message(
                "First name can not include special characters or numbers"
            ),
            "First-name validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_invalid_last_name_expects_validation_feedback(admission_flow) -> None:
    """Verify the last-name field rejects numeric input."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form with an invalid last name"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.fill_last_name("123")
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the invalid last-name validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message(
                "Last name can not include special characters or numbers"
            ),
            "Last-name validation should be visible",
        ).is_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    ("weight", "expected_message"),
    [
        ("0", "Weight must be between 10-250 kg"),
        ("1000", "Weight must be between 10-250 kg"),
    ],
)
def test_weight_boundaries_expect_validation_feedback(admission_flow, weight: str, expected_message: str) -> None:
    """Verify the weight field rejects values outside the supported live range."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step(f"Submit the form with weight '{weight}'"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.fill_weight(weight)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the weight validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message(expected_message),
            "Weight validation should be visible",
        ).is_visible()


@pytest.mark.ui
@pytest.mark.parametrize(
    ("height", "expected_message"),
    [
        ("0", "Height must be between 30-242 cm"),
        ("300", "Height must be between 30-242 cm"),
    ],
)
def test_height_boundaries_expect_validation_feedback(admission_flow, height: str, expected_message: str) -> None:
    """Verify the height field rejects values outside the supported live range."""
    data = build_happy_path_admission()

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step(f"Submit the form with height '{height}'"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.fill_height(height)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the height validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message(expected_message),
            "Height validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_missing_physician_expects_validation_feedback(admission_flow) -> None:
    """Verify the form requires a referring physician before submission."""
    data = PatientAdmissionData(
        patient_id=build_happy_path_admission().patient_id,
        device_id="676767",
        gender_at_birth="Male",
        first_name="Auto",
        last_name="Test",
        weight="70",
        height="170",
    )

    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit the form without selecting a referring physician"):
        admission_flow.patient_admission_page.fill_form(data)
        admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the missing physician validation message"):
        assert_that(
            admission_flow.patient_admission_page.get_validation_message("Referring physician is required"),
            "Referring physician validation should be visible",
        ).is_visible()
