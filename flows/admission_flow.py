from __future__ import annotations

from playwright.sync_api import Page

from config.settings import Settings
from test_data.patient_admission_cases import PatientAdmissionData
from ui.page_factory import PageObjectFactory
from ui.pages.auth.login_page import LoginPage
from ui.pages.patient_admission.patient_admission_page import PatientAdmissionPage
from ui.pages.patient_lookup.patient_lookup_page import PatientLookupPage
from ui.pages.session_management.session_management_page import SessionManagementPage
from ui.pages.shell.app_shell_page import AppShellPage


class PatientAdmissionFlow:
    """Wraps the repeated multi-page admission journey used by the live E2E tests.

    We keep this flow so tests do not have to repeat the same cross-page sequence:
    login -> navigate through the app shell -> open Patient Admission -> submit the
    form -> confirm the patient ID popup -> land back on Session Management.

    Page objects still own the screen-level locators and actions. This class only
    coordinates that shared business workflow in one place.
    """

    def __init__(self, page: Page, page_factory: PageObjectFactory, settings: Settings) -> None:
        self.page = page
        self.page_factory = page_factory
        self.settings = settings

    @property
    def login_page(self) -> LoginPage:
        return self.page_factory.create(LoginPage, self.page)

    @property
    def app_shell_page(self) -> AppShellPage:
        return self.page_factory.create(AppShellPage, self.page)

    @property
    def patient_admission_page(self) -> PatientAdmissionPage:
        return self.page_factory.create(PatientAdmissionPage, self.page)

    @property
    def session_management_page(self) -> SessionManagementPage:
        return self.page_factory.create(SessionManagementPage, self.page)

    @property
    def patient_lookup_page(self) -> PatientLookupPage:
        return self.page_factory.create(PatientLookupPage, self.page)

    def login_as_default_user(self) -> None:
        self.login_page.open()
        self.login_page.wait_until_ready()
        self.login_page.login(self.settings.username, self.settings.password)
        self.app_shell_page.wait_until_ready()
        self.session_management_page.wait_until_ready()

    def start_patient_admission(self) -> None:
        self.login_as_default_user()
        self.open_patient_admission()

    def open_patient_admission(self) -> None:
        self.app_shell_page.open_patient_admission()
        self.patient_admission_page.wait_until_ready()

    def open_session_management(self) -> None:
        self.app_shell_page.open_session_management()
        self.session_management_page.wait_until_ready()

    def open_patient_lookup(self) -> None:
        self.app_shell_page.open_patient_lookup()
        self.patient_lookup_page.wait_until_ready()

    def submit_admission(self, data: PatientAdmissionData) -> None:
        self.patient_admission_page.fill_form(data)
        confirmation_popup = self.patient_admission_page.submit_for_confirmation()
        confirmation_popup.fill_patient_id(data.patient_id)
        confirmation_popup.click_confirm()
        self.session_management_page.wait_for_url("**/session-management")
        self.session_management_page.wait_until_ready()
