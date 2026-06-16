import pytest
from playwright.sync_api import Page

from flows.admission_flow import PatientAdmissionFlow


@pytest.fixture(autouse=True)
def require_live_app_credentials(settings) -> None:
    """Skip the live UI suite when the BioBeat tenant credentials are not configured."""
    if not settings.has_app_credentials:
        pytest.skip("BioBeat UI credentials are not configured for this run.")


@pytest.fixture
def admission_flow(page: Page, page_factory, settings) -> PatientAdmissionFlow:
    """Provide the shared flow object used by navigation and admission tests."""
    return PatientAdmissionFlow(page=page, page_factory=page_factory, settings=settings)
