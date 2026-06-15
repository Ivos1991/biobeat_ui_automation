from __future__ import annotations

import allure
import pytest

from utils.assertions import assert_that


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.collect_all_evidence
def test_admission_happy_path_expects_pending_session_created_in_session_management(admission_flow,managed_admission) -> None:
    with allure.step("Login and open Patient Admission"):
        admission_flow.start_patient_admission()

    with allure.step("Submit a valid patient admission"):
        admission_flow.submit_admission(managed_admission.data)

    with allure.step("Verify the created session is visible in Session Management"):
        admission_flow.session_management_page.search_session(managed_admission.data.patient_id)
        row_text = admission_flow.session_management_page.get_row_text(managed_admission.data.patient_id)
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
