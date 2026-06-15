from __future__ import annotations

import pytest
from playwright.sync_api import Page

from flows.admission_flow import PatientAdmissionFlow
from utils.assertions import assert_that


@pytest.fixture
def admission_flow(page: Page, page_factory, settings) -> PatientAdmissionFlow:
    assert_that(
        settings.has_app_credentials,
        "Live UI credentials must be configured for patient admission tests",
    ).is_true()
    return PatientAdmissionFlow(page=page, page_factory=page_factory, settings=settings)
