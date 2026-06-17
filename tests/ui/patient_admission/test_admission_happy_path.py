import allure
import pytest

from flows.admission_flow import NoAvailableCreationDeviceError, PatientAdmissionFlow
from test_data.patient_admission_cases import build_complete_admission
from tests.ui.patient_admission.support import ManagedAdmission, skip_when_creation_is_blocked
from utils.assertions import assert_that


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.collect_all_evidence
def test_admission_happy_path_expects_pending_session_created_in_session_management(
    ready_admission_flow: PatientAdmissionFlow,
    managed_admission: ManagedAdmission,
) -> None:
    """Verify the real happy path from admission submission to visible pending session creation."""
    with allure.step("Submit a valid patient admission"):
        try:
            ready_admission_flow.submit_admission(managed_admission.data)
        except NoAvailableCreationDeviceError as error:
            pytest.skip(str(error))
        skip_when_creation_is_blocked(ready_admission_flow)

    with allure.step("Verify the created session is visible in Session Management"):
        ready_admission_flow.session_management_page.search_session(managed_admission.data.patient_id)
        row_text = ready_admission_flow.session_management_page.get_row_text(managed_admission.data.patient_id)
        assert_that(
            row_text,
            "Created patient ID should appear in Session Management",
        ).contains(managed_admission.data.patient_id)
        assert_that(
            row_text,
            "Created device ID should appear in Session Management",
        ).contains(managed_admission.data.device_id)
        assert_that(
            row_text,
            "Created session should appear with Pending status",
        ).contains("Pending")


@pytest.mark.ui
def test_admission_with_valid_date_of_birth_expects_pending_session_created(
    ready_admission_flow: PatientAdmissionFlow,
    managed_admission: ManagedAdmission,
) -> None:
    """Verify a valid Date of Birth still allows a real patient admission to be created."""
    managed_admission.data = build_complete_admission(
        patient_id=managed_admission.data.patient_id,
        device_id=managed_admission.data.device_id,
        date_of_birth="01/01/2000",
    )

    with allure.step("Submit a valid patient admission that includes Date of Birth"):
        try:
            ready_admission_flow.submit_admission(managed_admission.data)
        except NoAvailableCreationDeviceError as error:
            pytest.skip(str(error))
        skip_when_creation_is_blocked(ready_admission_flow)

    with allure.step("Verify the created session is visible in Session Management"):
        ready_admission_flow.session_management_page.search_session(managed_admission.data.patient_id)
        assert_that(
            ready_admission_flow.session_management_page.has_session(managed_admission.data.patient_id),
            "The Date-of-Birth admission should appear in Session Management",
        ).is_true()
