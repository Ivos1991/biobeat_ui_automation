import allure
import pytest

from tests.ui.patient_admission.support import build_managed_admission, cleanup_session_by_patient_id
from ui.pages.session_management.session_management_page import SessionManagementPage
from utils.assertions import assert_that


@pytest.fixture
def managed_admission(page, page_factory):
    """Create unique admission data and tear down any created session after the test finishes."""
    context = build_managed_admission()
    yield context

    if not context.cleanup_required:
        return

    session_page = page_factory.create(SessionManagementPage, page)

    with allure.step(f"Navigate to Session Management for teardown cleanup of '{context.data.patient_id}'"):
        session_page.goto("/session-management")
        session_page.wait_until_ready()

    with allure.step(f"Run idempotent cleanup for patient '{context.data.patient_id}'"):
        removed = cleanup_session_by_patient_id(session_page, context.data.patient_id)
        assert_that(
            removed or not session_page.has_session(context.data.patient_id),
            f"Cleanup should leave no visible session for patient '{context.data.patient_id}'",
        ).is_true()
