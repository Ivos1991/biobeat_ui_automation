from __future__ import annotations

import allure
import pytest

from utils.assertions import assert_that


@pytest.mark.ui
@pytest.mark.smoke
def test_navigation_to_patient_admission_expects_form_to_load(admission_flow) -> None:
    with allure.step("Login with the default BioBeat user"):
        admission_flow.login_as_default_user()

    with allure.step("Navigate to Patient Admission"):
        admission_flow.open_patient_admission()

    with allure.step("Verify the Patient Admission page is ready"):
        assert_that(
            admission_flow.patient_admission_page.patient_id_input,
            "Patient ID input should be visible on Patient Admission",
        ).is_visible()
        assert_that(
            admission_flow.patient_admission_page.device_id_input,
            "Device ID input should be visible on Patient Admission",
        ).is_visible()
        assert_that(
            admission_flow.patient_admission_page.current_url,
            "Navigation should reach the Patient Admission route",
        ).contains("/patient-admission")


@pytest.mark.ui
def test_navigation_to_patient_lookup_expects_search_and_table_to_load(admission_flow) -> None:
    with allure.step("Login with the default BioBeat user"):
        admission_flow.login_as_default_user()

    with allure.step("Navigate to Patient Lookup"):
        admission_flow.open_patient_lookup()

    with allure.step("Verify the Patient Lookup page is ready"):
        assert_that(
            admission_flow.patient_lookup_page.search_patient_input,
            "Patient Lookup search input should be visible",
        ).is_visible()
        assert_that(
            admission_flow.patient_lookup_page.patient_table,
            "Patient Lookup table should be visible",
        ).is_visible()
        assert_that(
            admission_flow.patient_lookup_page.current_url,
            "Navigation should reach the Patient Lookup route",
        ).contains("/patient-lookup")
