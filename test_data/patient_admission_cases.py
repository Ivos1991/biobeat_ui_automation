from dataclasses import dataclass
from uuid import uuid4


@dataclass(slots=True)
class PatientAdmissionData:
    """Structured admission payload shared by happy-path and validation tests."""
    patient_id: str
    device_id: str
    gender_at_birth: str | None = None
    referring_physician: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: str | None = None
    weight: str | None = None
    height: str | None = None
    additional_notes: str | None = None
    receive_report_completion_emails: bool = False


def build_unique_patient_id(prefix: str = "AUTO") -> str:
    """Generate a unique patient ID so live runs do not collide with prior sessions."""
    return f"{prefix}{uuid4().hex[:12].upper()}"


def build_happy_path_admission(device_id: str = "676767") -> PatientAdmissionData:
    """Build the default valid admission payload used by most live-flow tests."""
    return PatientAdmissionData(
        patient_id=build_unique_patient_id(),
        device_id=device_id,
        gender_at_birth="Male",
        referring_physician="chen.nahoom",
        first_name="Auto",
        last_name="Test",
        weight="70",
        height="170",
        additional_notes="Created by live BioBeat UI automation.",
    )
