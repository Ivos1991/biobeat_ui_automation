from core.framework.types import EvidenceMode


def should_capture_trace(evidence_mode: EvidenceMode, collect_all_evidence: bool) -> bool:
    """Decide whether Playwright tracing should be enabled for the current run."""
    return collect_all_evidence or evidence_mode in {"full", "failure_only"}


def should_record_video(evidence_mode: EvidenceMode, collect_all_evidence: bool) -> bool:
    """Decide whether Playwright video recording should be enabled for the current run."""
    return collect_all_evidence or evidence_mode in {"full", "failure_only"}


def should_attach_test_evidence(evidence_mode: EvidenceMode, collect_all_evidence: bool, test_failed: bool) -> bool:
    """Decide whether collected evidence should be attached to the current test in Allure."""
    if collect_all_evidence or evidence_mode == "full":
        return True
    if evidence_mode in {"failure_only", "screenshot_only"}:
        return test_failed
    return False
