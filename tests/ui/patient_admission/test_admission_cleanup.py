import allure
import pytest

from flows.admission_flow import NoAvailableCreationDeviceError, PatientAdmissionFlow
from tests.ui.patient_admission.support import (
    ManagedAdmission,
    cleanup_session_by_patient_id,
    skip_when_creation_is_blocked,
    wait_for_session_to_disappear,
)
from utils.assertions import assert_that


@pytest.mark.ui
def test_cleanup_expects_session_removal_to_require_patient_id_and_be_idempotent(
    ready_admission_flow: PatientAdmissionFlow,
    managed_admission: ManagedAdmission,
) -> None:
    """Verify live removal rules and prove teardown cleanup stays safe on repeated attempts."""
    with allure.step("Create a real admission that can later be removed"):
        try:
            ready_admission_flow.submit_admission(managed_admission.data)
        except NoAvailableCreationDeviceError as error:
            pytest.skip(str(error))
        skip_when_creation_is_blocked(ready_admission_flow)

    with allure.step("Verify the created session is present before removal"):
        ready_admission_flow.session_management_page.search_session(managed_admission.data.patient_id)
        assert_that(
            ready_admission_flow.session_management_page.has_session(managed_admission.data.patient_id),
            "Created session should be visible in Session Management before cleanup",
        ).is_true()

    with allure.step("Open the Remove Session popup and verify patient-ID confirmation behavior"):
        remove_popup = ready_admission_flow.session_management_page.open_remove_session_popup(
            managed_admission.data.patient_id
        )
        assert_that(
            remove_popup,
            "Remove Session popup should open for the created session",
        ).is_not_none()
        assert remove_popup is not None
        popup = remove_popup
        assert_that(
            popup.remove_button,
            "Remove button should start disabled in the Remove Session popup",
        ).is_disabled()
        popup.fill_patient_id_confirmation("wrong-value")
        assert_that(
            popup.remove_button,
            "Remove button should remain disabled for the wrong patient ID",
        ).is_disabled()
        popup.fill_patient_id_confirmation("")
        assert_that(
            popup.remove_button,
            "Remove button should remain disabled for an empty patient ID",
        ).is_disabled()
        popup.fill_patient_id_confirmation(managed_admission.data.patient_id)
        assert_that(
            popup.remove_button,
            "Remove button should enable for the exact patient ID",
        ).is_enabled()

    with allure.step("Remove the created session and verify it disappears"):
        popup.click_remove()
        assert_that(
            wait_for_session_to_disappear(
                ready_admission_flow.session_management_page,
                managed_admission.data.patient_id,
            ),
            "The session should no longer be visible after manual removal",
        ).is_true()

    with allure.step("Verify teardown cleanup remains idempotent after manual removal"):
        removed = cleanup_session_by_patient_id(
            ready_admission_flow.session_management_page,
            managed_admission.data.patient_id,
        )
        assert_that(
            removed,
            "A second cleanup attempt should be a safe no-op when the session is already removed",
        ).is_false()
