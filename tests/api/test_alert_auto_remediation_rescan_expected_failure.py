import allure
import pytest
from assertpy import assert_that
from core.framework.types import AlertStatus


@pytest.mark.api
@pytest.mark.expected_failure
@pytest.mark.xfail(
    strict=True,
    reason="The application intentionally re-detects the same auto-remediated issue after resolve + rescan.",
)
def test_auto_remediation_rescan_expects_no_duplicate_alert_and_currently_fails(alert_workflows, scans_service, alerts_service):
    with allure.step("Start initial scan and wait for alert creation"):
        bundle = alert_workflows.create_auto_remediating_alert()
        first_scan = bundle.scan

    with allure.step("Find an auto-remediating alert in OPEN or REMEDIATION_IN_PROGRESS"):
        target_alert = bundle.alert

    with allure.step("Wait for remediation completion if needed"):
        if target_alert.status != AlertStatus.REMEDIATED_WAITING_FOR_CUSTOMER.value:
            target_alert = alerts_service.wait_for_status(
                target_alert.id,
                {AlertStatus.REMEDIATED_WAITING_FOR_CUSTOMER})

    with allure.step("Resolve the alert and add verification comment"):
        resolved_alert = alerts_service.update_alert(target_alert.id, status=AlertStatus.RESOLVED)
        alerts_service.add_comment(
            resolved_alert.id,
            "Remediation verified successfully and issue is resolved")

    with allure.step("Start a second scan"):
        second_scan = scans_service.start_scan()
        scans_service.wait_for_completion(second_scan.id)

    with allure.step("Verify that no identical alert was created by the second scan"):
        second_scan_alerts = alerts_service.list_alerts(runId=second_scan.id)
        duplicates = [alert for alert in second_scan_alerts if alert.matches_signature(resolved_alert)]

        assert_that(duplicates).described_as(
            "no identical alert should be created after remediation and rescan").is_empty()
