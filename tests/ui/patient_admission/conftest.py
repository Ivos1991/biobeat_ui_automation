import pytest

from flows.admission_flow import PatientAdmissionFlow
from tests.ui.patient_admission.support import (
    ManagedAdmission,
    build_managed_admission,
)


@pytest.fixture
def managed_admission() -> ManagedAdmission:
    """Create unique admission data for tests that need a real patient admission payload."""
    return build_managed_admission()


@pytest.fixture
def ready_admission_flow(admission_flow: PatientAdmissionFlow) -> PatientAdmissionFlow:
    """Open Patient Admission with an authenticated user so scenario tests stay declarative."""
    admission_flow.start_patient_admission()
    return admission_flow
