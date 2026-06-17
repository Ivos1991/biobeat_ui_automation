import allure
from playwright.sync_api import Page

from config.settings import Settings
from test_data.patient_admission_cases import ASSIGNMENT_CREATION_DEVICE_IDS, PatientAdmissionData
from ui.page_factory import PageObjectFactory
from ui.pages.auth.login_page import LoginPage
from ui.pages.patient_admission.patient_admission_page import PatientAdmissionPage
from ui.pages.patient_lookup.patient_lookup_page import PatientLookupPage
from ui.pages.session_management.session_management_page import SessionManagementPage
from ui.pages.shell.app_shell_page import AppShellPage


class NoAvailableCreationDeviceError(RuntimeError):
    """Raised when every known-good assignment device is temporarily unavailable."""


class PatientAdmissionFlow:
    """Wraps the repeated multi-page admission journey used by the live E2E tests.

    We keep this flow so tests do not have to repeat the same cross-page sequence:
    login -> navigate through the app shell -> open Patient Admission -> submit the
    form -> confirm the patient ID popup -> land back on Session Management.

    Page objects still own the screen-level locators and actions. This class only
    coordinates that shared business workflow in one place.
    """

    def __init__(self, page: Page, page_factory: PageObjectFactory, settings: Settings) -> None:
        """Store the shared dependencies needed to orchestrate the admission journey."""
        self.page = page
        self.page_factory = page_factory
        self.settings = settings
        self.created_patient_ids: list[str] = []

    @property
    def login_page(self) -> LoginPage:
        """Return the login page object bound to the active Playwright page."""
        return self.page_factory.create(LoginPage, self.page)

    @property
    def app_shell_page(self) -> AppShellPage:
        """Return the shared authenticated shell used for left-menu navigation."""
        return self.page_factory.create(AppShellPage, self.page)

    @property
    def patient_admission_page(self) -> PatientAdmissionPage:
        """Return the page object for the Patient Admission form."""
        return self.page_factory.create(PatientAdmissionPage, self.page)

    @property
    def session_management_page(self) -> SessionManagementPage:
        """Return the page object for the Session Management screen."""
        return self.page_factory.create(SessionManagementPage, self.page)

    @property
    def patient_lookup_page(self) -> PatientLookupPage:
        """Return the page object for the Patient Lookup screen."""
        return self.page_factory.create(PatientLookupPage, self.page)

    def login_as_default_user(self) -> None:
        """Authenticate with the configured BioBeat credentials and wait for the landing screen."""
        with allure.step("Open /login"):
            self.login_page.open()
            self.login_page.wait_until_ready()

        with allure.step("Submit BioBeat credentials"):
            self.login_page.login(self.settings.username, self.settings.password)

        with allure.step("Wait for Session Management to load after login"):
            self.app_shell_page.wait_until_ready()
            self.session_management_page.wait_until_ready()

    def start_patient_admission(self) -> None:
        """Perform the standard login-and-navigation sequence needed before admission tests."""
        self.login_as_default_user()
        self.open_patient_admission()

    def open_patient_admission(self) -> None:
        """Navigate from the authenticated shell into Patient Admission."""
        with allure.step("Open Patient Admission from the side menu"):
            self.app_shell_page.open_patient_admission()

        with allure.step("Wait for Patient Admission to finish loading"):
            self.patient_admission_page.wait_until_ready()

    def open_session_management(self) -> None:
        """Navigate from the authenticated shell into Session Management."""
        with allure.step("Open Session Management from the side menu"):
            self.app_shell_page.open_session_management()

        with allure.step("Wait for Session Management to finish loading"):
            self.session_management_page.wait_until_ready()

    def open_patient_lookup(self) -> None:
        """Navigate from the authenticated shell into Patient Lookup."""
        with allure.step("Open Patient Lookup from the side menu"):
            self.app_shell_page.open_patient_lookup()

        with allure.step("Wait for Patient Lookup to finish loading"):
            self.patient_lookup_page.wait_until_ready()

    def _candidate_creation_device_ids(self, preferred_device_id: str) -> tuple[str, ...]:
        """Return the preferred valid assignment device first, followed by any known fallback devices."""
        fallbacks = tuple(device_id for device_id in ASSIGNMENT_CREATION_DEVICE_IDS if device_id != preferred_device_id)
        return (preferred_device_id, *fallbacks)

    def register_created_session(self, patient_id: str) -> None:
        """Track successfully created sessions so fixture teardown can always remove them."""
        if patient_id not in self.created_patient_ids:
            self.created_patient_ids.append(patient_id)

    def submit_admission(self, data: PatientAdmissionData) -> None:
        """Submit a fully populated admission and finish the confirmation-popup handshake."""
        candidate_device_ids = self._candidate_creation_device_ids(data.device_id)

        for attempt_index, device_id in enumerate(candidate_device_ids, start=1):
            data.device_id = device_id

            with allure.step(f"Fill the Patient Admission form with candidate device '{device_id}'"):
                if attempt_index == 1:
                    self.patient_admission_page.fill_form(data)
                else:
                    self.patient_admission_page.fill_device_id(device_id)

            with allure.step("Open the patient-ID confirmation popup"):
                confirmation_popup = self.patient_admission_page.submit_for_confirmation()

            with allure.step("Confirm the admission with the same Patient ID"):
                confirmation_popup.fill_patient_id(data.patient_id)
                confirmation_popup.click_confirm()

            with allure.step("Wait for the admission result and open Session Management on success"):
                self.patient_admission_page.wait_for_submission_result()
                if "/session-management" in self.page.url:
                    self.register_created_session(data.patient_id)
                    self.session_management_page.wait_until_ready()
                    return

                body_text = self.page.locator("body").inner_text()
                if "Device is in use." in body_text and attempt_index < len(candidate_device_ids):
                    continue

                blocking_feedback = (
                    "Please correct form errors",
                    "Error admitting this patient",
                    "Device is in use.",
                    "Device is not activated or does not exist.",
                )
                if any(message in body_text for message in blocking_feedback):
                    if "Device is in use." in body_text:
                        raise NoAvailableCreationDeviceError(
                            "No known-good assignment device is currently available for session creation."
                        )
                    return
                self.register_created_session(data.patient_id)
                self.open_session_management()
                return
