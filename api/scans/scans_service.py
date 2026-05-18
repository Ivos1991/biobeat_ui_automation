"""Scan orchestration service layer."""

from assertpy import assert_that

from api.scans.scans_api import ScansApi
from api.scans.scans_response import ScanResponse
from config.settings import Settings
from core.core_utils.logger import get_logger
from core.core_utils.retry_utils import wait_until
from core.framework.decorators import logged_call, timed_call
from core.framework.types import ScanId, ScanStatus


class ScansService:
    """Business service for managing platform scans."""

    def __init__(self, scans_api: ScansApi, settings: Settings) -> None:
        self.scans_api = scans_api
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)

    @logged_call("Start scan")
    @timed_call("scans.start_scan")
    def start_scan(self) -> ScanResponse:
        response = ScanResponse.from_dict(self.scans_api.start_scan())
        assert_that(response.status).described_as("newly started scan should be running").is_equal_to(
            ScanStatus.RUNNING.value
        )
        return response

    def list_scans(self) -> list[ScanResponse]:
        return [ScanResponse.from_dict(item) for item in self.scans_api.list_scans() or []]

    def get_scan(self, scan_id: ScanId | str) -> ScanResponse:
        return ScanResponse.from_dict(self.scans_api.get_scan(str(scan_id)))

    @logged_call("Wait for scan completion")
    @timed_call("scans.wait_for_completion")
    def wait_for_completion(self, scan_id: ScanId | str) -> ScanResponse:
        def _fetch() -> ScanResponse | None:
            scan = self.get_scan(scan_id)
            return scan if scan.status == ScanStatus.COMPLETED.value else None

        completed_scan = wait_until(
            _fetch,
            timeout_seconds=self.settings.poll_timeout_seconds,
            interval_seconds=self.settings.poll_interval_seconds,
            description=f"scan {scan_id} to complete",
        )
        assert_that(completed_scan.alerts_created_count).described_as(
            "completed scan should report created alerts"
        ).is_greater_than_or_equal_to(0)
        return completed_scan
