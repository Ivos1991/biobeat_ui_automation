from __future__ import annotations

import pytest
from playwright.sync_api import Page

from flows.admission_flow import PatientAdmissionFlow


@pytest.fixture(autouse=True)
def require_live_app_credentials(settings) -> None:
    if not settings.has_app_credentials:
        pytest.skip("BioBeat UI credentials are not configured for this run.")


@pytest.fixture
def admission_flow(page: Page, page_factory, settings) -> PatientAdmissionFlow:
    return PatientAdmissionFlow(page=page, page_factory=page_factory, settings=settings)
