"""Composable alert lifecycle orchestrators."""

from dataclasses import dataclass

from api.alerts.alerts_service import AlertsService
from api.alerts.alerts_response import AlertResponse
from api.scans.scans_response import ScanResponse
from api.scans.scans_service import ScansService
from core.framework.types import AlertStatus


@dataclass(slots=True)
class ScanAlertBundle:
    scan: ScanResponse
    alert: AlertResponse


class AlertWorkflowOrchestrator:
    """Coordinates cross-service alert setup flows for tests."""

    def __init__(self, scans_service: ScansService, alerts_service: AlertsService) -> None:
        self.scans_service = scans_service
        self.alerts_service = alerts_service

    def create_manual_alert(self) -> ScanAlertBundle:
        scan = self.scans_service.start_scan()
        self.scans_service.wait_for_completion(scan.id)
        alert = self.alerts_service.find_alert(statuses={AlertStatus.OPEN}, auto_remediate=False)
        return ScanAlertBundle(scan=scan, alert=alert)

    def create_auto_remediating_alert(self) -> ScanAlertBundle:
        scan = self.scans_service.start_scan()
        self.scans_service.wait_for_completion(scan.id)
        alert = self.alerts_service.find_alert(
            statuses={AlertStatus.OPEN, AlertStatus.REMEDIATION_IN_PROGRESS},
            auto_remediate=True,
        )
        return ScanAlertBundle(scan=scan, alert=alert)
