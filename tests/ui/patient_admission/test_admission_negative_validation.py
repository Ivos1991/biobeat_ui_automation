import allure
import pytest

from flows.admission_flow import PatientAdmissionFlow
from test_data.patient_admission_cases import PatientAdmissionData, build_complete_admission, build_happy_path_admission
from tests.ui.patient_admission.support import (
    DEVICE_NOT_ACTIVATED_ID,
    ManagedAdmission,
    skip_when_creation_is_blocked,
)
from utils.assertions import assert_that


@pytest.mark.ui
def test_missing_required_patient_id_expects_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the form blocks submission when Patient ID is missing."""
    data = build_happy_path_admission()

    with allure.step("Submit the form without Patient ID"):
        ready_admission_flow.patient_admission_page.fill_required_fields(patient_id=None, device_id=data.device_id)
        ready_admission_flow.patient_admission_page.fill_optional_fields(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the Patient ID required validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message("Patient ID is required"),
            "Patient ID required validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_missing_required_device_id_expects_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the form blocks submission when Device ID is missing."""
    data = build_happy_path_admission()

    with allure.step("Submit the form without Device ID"):
        ready_admission_flow.patient_admission_page.fill_required_fields(patient_id=data.patient_id, device_id=None)
        ready_admission_flow.patient_admission_page.fill_optional_fields(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the Device ID required validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message("Device ID is required"),
            "Device ID required validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_device_shorter_than_minimum_expects_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the Device ID minimum-length validation using a too-short live input."""
    data = build_happy_path_admission(device_id="9")

    with allure.step("Submit the form with a device ID shorter than the minimum length"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the short Device ID validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "Device ID must be at least 4 characters"
            ),
            "Short Device ID validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_device_already_assigned_expects_in_use_feedback(
    ready_admission_flow: PatientAdmissionFlow,
    managed_admission: ManagedAdmission,
) -> None:
    """Verify a device already assigned to a live session cannot be assigned to another patient."""
    with allure.step("Create a real session with an available assignment device"):
        ready_admission_flow.submit_admission(managed_admission.data)
        skip_when_creation_is_blocked(ready_admission_flow)

    retry_data = build_complete_admission(device_id=managed_admission.data.device_id)

    with allure.step("Attempt to assign the same device to a second patient"):
        ready_admission_flow.open_patient_admission()
        ready_admission_flow.patient_admission_page.fill_form(retry_data)
        popup = ready_admission_flow.patient_admission_page.submit_for_confirmation()
        popup.fill_patient_id(retry_data.patient_id)
        popup.click_confirm()

    with allure.step("Verify the live device-in-use message is shown and the user stays on the form"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message("Device is in use."),
            "Device-in-use validation should be visible after final confirmation",
        ).is_visible()
        assert_that(
            ready_admission_flow.patient_admission_page.current_url,
            "The user should remain on Patient Admission when reusing an assigned device",
        ).contains("/patient-admission")


@pytest.mark.ui
def test_device_not_activated_expects_distinct_feedback(ready_admission_flow: PatientAdmissionFlow) -> None:
    """Verify an ineligible device state maps to the distinct not-activated feedback."""
    data = build_happy_path_admission(device_id=DEVICE_NOT_ACTIVATED_ID)

    with allure.step(f"Submit the form with device '{DEVICE_NOT_ACTIVATED_ID}'"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        popup = ready_admission_flow.patient_admission_page.submit_for_confirmation()
        popup.fill_patient_id(data.patient_id)
        popup.click_confirm()

    with allure.step("Verify the not-activated device message on Patient Admission"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "Device is not activated or does not exist."
            ),
            "Not-activated device validation should be visible after final confirmation",
        ).is_visible()
        assert_that(
            ready_admission_flow.patient_admission_page.current_url,
            "The user should remain on Patient Admission when the device is not eligible",
        ).contains("/patient-admission")


@pytest.mark.ui
def test_invalid_first_name_expects_validation_feedback(ready_admission_flow: PatientAdmissionFlow) -> None:
    """Verify the first-name field rejects numeric input."""
    data = build_happy_path_admission()

    with allure.step("Submit the form with an invalid first name"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.fill_first_name("123")
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the invalid first-name validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "First name can not include special characters or numbers"
            ),
            "First-name validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_invalid_last_name_expects_validation_feedback(ready_admission_flow: PatientAdmissionFlow) -> None:
    """Verify the last-name field rejects numeric input."""
    data = build_happy_path_admission()

    with allure.step("Submit the form with an invalid last name"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.fill_last_name("123")
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the invalid last-name validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
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
def test_weight_boundaries_expect_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
    weight: str,
    expected_message: str,
) -> None:
    """Verify the weight field rejects values outside the supported live range."""
    data = build_happy_path_admission()

    with allure.step(f"Submit the form with weight '{weight}'"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.fill_weight(weight)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the weight validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(expected_message),
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
def test_height_boundaries_expect_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
    height: str,
    expected_message: str,
) -> None:
    """Verify the height field rejects values outside the supported live range."""
    data = build_happy_path_admission()

    with allure.step(f"Submit the form with height '{height}'"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.fill_height(height)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the height validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(expected_message),
            "Height validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_missing_physician_expects_validation_feedback(ready_admission_flow: PatientAdmissionFlow) -> None:
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

    with allure.step("Submit the form without selecting a referring physician"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the missing physician validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message("Referring physician is required"),
            "Referring physician validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_invalid_patient_id_characters_expect_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify the Patient ID field rejects special characters."""
    data = build_happy_path_admission()
    data.patient_id = "@@@"

    with allure.step("Submit the form with an invalid Patient ID format"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the invalid Patient ID validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "Patient ID can only contain numbers and letters"
            ),
            "Patient ID format validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_future_date_of_birth_expects_validation_feedback(ready_admission_flow: PatientAdmissionFlow) -> None:
    """Verify a future Date of Birth is rejected by the form."""
    data = build_complete_admission(date_of_birth="01/01/2099")

    with allure.step("Submit the form with a future Date of Birth"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the future Date of Birth validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "Date of birth cannot be in the future"
            ),
            "Future Date-of-Birth validation should be visible",
        ).is_visible()


@pytest.mark.ui
def test_additional_notes_invalid_characters_expect_validation_feedback(
    ready_admission_flow: PatientAdmissionFlow,
) -> None:
    """Verify unsupported special characters in Additional Notes are rejected cleanly."""
    data = build_complete_admission(
        additional_notes="Special characters < > $ ^ are not allowed?",
    )

    with allure.step("Submit the form with unsupported special characters in Additional Notes"):
        ready_admission_flow.patient_admission_page.fill_form(data)
        ready_admission_flow.patient_admission_page.click_confirm()

    with allure.step("Verify the Additional Notes validation message"):
        assert_that(
            ready_admission_flow.patient_admission_page.get_validation_message(
                "Special characters < > $ ^ are not allowed."
            ),
            "Additional Notes validation should be visible",
        ).is_visible()
