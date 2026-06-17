from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import Page

from config.settings import Settings
from flows.admission_flow import PatientAdmissionFlow
from test_data.patient_admission_cases import generated_patient_id_count, generated_patient_ids_since
from tests.ui.patient_admission.support import cleanup_session_by_patient_id
from ui.page_factory import PageObjectFactory
from ui.pages.session_management.session_management_page import SessionManagementPage


@pytest.fixture(autouse=True)
def require_live_app_credentials(settings: Settings) -> None:
    """Skip the live UI suite when the BioBeat tenant credentials are not configured."""
    if not settings.has_app_credentials:
        pytest.skip("BioBeat UI credentials are not configured for this run.")


@pytest.fixture
def admission_flow(
    page: Page,
    page_factory: PageObjectFactory,
    settings: Settings,
) -> Generator[PatientAdmissionFlow, None, None]:
    """Provide the shared flow object and always clean up any created sessions in teardown."""
    flow = PatientAdmissionFlow(page=page, page_factory=page_factory, settings=settings)
    yield flow

    if not flow.created_patient_ids:
        return

    session_page = page_factory.create(SessionManagementPage, page)
    with allure.step("Navigate to Session Management for flow teardown cleanup"):
        session_page.goto("/session-management")
        session_page.wait_until_ready()

    for patient_id in reversed(flow.created_patient_ids):
        with allure.step(f"Run flow teardown cleanup for patient '{patient_id}'"):
            removed = cleanup_session_by_patient_id(session_page, patient_id)
            if not removed and session_page.has_session(patient_id):
                raise AssertionError(f"Teardown could not remove the created session for patient '{patient_id}'.")


@pytest.fixture(autouse=True)
def cleanup_generated_patient_ids(
    request: pytest.FixtureRequest,
    page: Page,
    page_factory: PageObjectFactory,
    settings: Settings,
) -> Generator[None, None, None]:
    """Clean up every generated AUTO patient ID after each test, even if the test fails mid-flow."""
    start_index = generated_patient_id_count()
    yield

    generated_ids = list(dict.fromkeys(generated_patient_ids_since(start_index)))
    if not generated_ids:
        return

    flow = PatientAdmissionFlow(page=page, page_factory=page_factory, settings=settings)
    session_page = page_factory.create(SessionManagementPage, page)

    with allure.step(f"Open Session Management for generated-patient cleanup of {request.node.name}"):
        try:
            session_page.goto("/session-management")
            session_page.wait_until_ready()
        except Exception:
            flow.login_as_default_user()
            flow.open_session_management()

    failures: list[str] = []
    for patient_id in reversed(generated_ids):
        with allure.step(f"Cleanup generated patient '{patient_id}'"):
            removed = cleanup_session_by_patient_id(session_page, patient_id)
            if not removed and session_page.has_session(patient_id):
                failures.append(patient_id)

    if failures:
        raise AssertionError(
            "Generated patient cleanup failed for: " + ", ".join(failures)
        )
