from dataclasses import dataclass
from uuid import uuid4

ASSIGNMENT_CREATION_DEVICE_IDS: tuple[str, str] = ("989898", "676767")
_GENERATED_PATIENT_IDS: list[str] = []


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
    patient_id = f"{prefix}{uuid4().hex[:12].upper()}"
    _GENERATED_PATIENT_IDS.append(patient_id)
    return patient_id


def generated_patient_id_count() -> int:
    """Return how many runtime-generated patient IDs have been issued in this process."""
    return len(_GENERATED_PATIENT_IDS)


def generated_patient_ids_since(index: int) -> list[str]:
    """Return the generated patient IDs created after the provided list index."""
    return _GENERATED_PATIENT_IDS[index:]


def build_happy_path_admission(device_id: str = ASSIGNMENT_CREATION_DEVICE_IDS[0]) -> PatientAdmissionData:
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


def build_complete_admission(
    *,
    patient_id: str | None = None,
    device_id: str = ASSIGNMENT_CREATION_DEVICE_IDS[0],
    gender_at_birth: str = "Male",
    referring_physician: str = "chen.nahoom",
    date_of_birth: str | None = None,
    additional_notes: str = "Created by live BioBeat UI automation.",
) -> PatientAdmissionData:
    """Build a fully valid admission payload while allowing focused overrides per scenario."""
    return PatientAdmissionData(
        patient_id=patient_id or build_unique_patient_id(),
        device_id=device_id,
        gender_at_birth=gender_at_birth,
        referring_physician=referring_physician,
        first_name="Auto",
        last_name="Test",
        date_of_birth=date_of_birth,
        weight="70",
        height="170",
        additional_notes=additional_notes,
    )
