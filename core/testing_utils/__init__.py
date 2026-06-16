from .evidence import should_attach_test_evidence, should_capture_trace, should_record_video
from .playwright_artifacts import attach_artifacts_from_output_path, attach_log_file, attach_page_screenshot

__all__ = [
    "attach_artifacts_from_output_path",
    "attach_log_file",
    "attach_page_screenshot",
    "should_attach_test_evidence",
    "should_capture_trace",
    "should_record_video",
]
