"""Page objects for the assignment UI."""
from ui.pages.auth.login_page import LoginPage
from ui.pages.patient_admission.exit_patient_admission_popup import ExitPatientAdmissionPopup
from ui.pages.patient_admission.patient_admission_confirmation_popup import PatientAdmissionConfirmationPopup
from ui.pages.patient_admission.patient_admission_page import PatientAdmissionPage
from ui.pages.patient_lookup.patient_lookup_page import PatientLookupPage
from ui.pages.session_management.remove_session_popup import RemoveSessionPopup
from ui.pages.session_management.session_management_page import SessionManagementPage
from ui.pages.shell.app_shell_page import AppShellPage

__all__ = [
    "AppShellPage",
    "ExitPatientAdmissionPopup",
    "LoginPage",
    "PatientAdmissionPage",
    "PatientAdmissionConfirmationPopup",
    "PatientLookupPage",
    "RemoveSessionPopup",
    "SessionManagementPage",
]
