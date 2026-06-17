from dataclasses import dataclass

import allure
import pytest

from flows.admission_flow import PatientAdmissionFlow
from test_data.patient_admission_cases import PatientAdmissionData, build_happy_path_admission
from ui.pages.session_management.remove_session_popup import RemoveSessionPopup
from ui.pages.session_management.session_management_page import SessionManagementPage
from utils.assertions import assert_that

CREATION_DEVICE_ID = "989898"
SECONDARY_CREATION_DEVICE_ID = "676767"
DEVICE_IN_USE_ID = "126875"
DEVICE_NOT_ACTIVATED_ID = "676733"


@dataclass(slots=True)
class ManagedAdmission:
    """Hold the generated admission data together with cleanup state for teardown."""
    data: PatientAdmissionData
    cleanup_required: bool = True


def build_managed_admission() -> ManagedAdmission:
    """Build the standard happy-path admission payload using the verified creation device."""
    return ManagedAdmission(data=build_happy_path_admission(device_id=CREATION_DEVICE_ID))


def wait_for_session_to_disappear(
    session_page: SessionManagementPage,
    patient_id: str,
    attempts: int = 6,
) -> bool:
    """Refresh and re-search until a removed session disappears from the live table."""
    # Session Management updates asynchronously after removals, so refresh and re-search
    # until the row is gone or we exhaust a small bounded retry window.
    with allure.step(f"Wait for session '{patient_id}' to disappear from Session Management"):
        for attempt_index in range(1, attempts + 1):
            with allure.step(f"Removal verification attempt {attempt_index} of {attempts}"):
                session_page.click_refresh()
                session_page.search_session(patient_id)
                if not session_page.has_session(patient_id):
                    return True
                session_page.wait_for_loading_to_finish()
    return False


def cleanup_session_by_patient_id(session_page: SessionManagementPage, patient_id: str) -> bool:
    """Remove a live session through the UI when it is still present in Session Management."""
    with allure.step(f"Search for session '{patient_id}' before cleanup"):
        session_page.search_session(patient_id)
        if not session_page.has_session(patient_id):
            return False

    with allure.step(f"Open remove-session popup for '{patient_id}'"):
        remove_popup = session_page.open_remove_session_popup(patient_id)
        assert_that(
            remove_popup,
            f"Remove Session popup should open for patient '{patient_id}'",
        ).is_not_none()

    popup = remove_popup or RemoveSessionPopup(session_page.page, session_page.settings, runtime=session_page.runtime)

    with allure.step(f"Confirm session removal for '{patient_id}' with the same patient ID"):
        # The live app enables removal only when the exact Patient ID is typed.
        popup.fill_patient_id_confirmation(patient_id)
        assert_that(
            popup.remove_button,
            "Remove button should enable when the exact patient ID is entered",
        ).is_enabled()
        popup.click_remove()

    with allure.step(f"Verify session '{patient_id}' is no longer visible in Session Management"):
        return wait_for_session_to_disappear(session_page, patient_id)


def skip_when_creation_is_blocked(flow: PatientAdmissionFlow) -> None:
    """Skip creation-dependent tests when the live tenant reports the documented device limitation."""
    body_text = flow.page.locator("body").inner_text()
    if "/session-management" not in flow.page.url and "Device is in use." in body_text:
        pytest.skip("No assignment device is currently available for this user in the live tenant.")
