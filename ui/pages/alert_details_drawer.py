import allure
from playwright.sync_api import Page, expect

from config.settings import Settings
from ui.pages.base_page import BasePage


class AlertDetailsDrawer(BasePage):
    def __init__(self, page: Page, settings: Settings, *, runtime=None) -> None:
        super().__init__(page, settings, runtime=runtime)
        self.root = page.get_by_test_id("alert-details-drawer")
        self.remediation_section_toggle = self.root.get_by_role("button", name="Remediation")
        self.status_button = self.root.get_by_role("button", name="Change alert status")
        self.assignee_button = self.root.get_by_role("button", name="Assign alert")
        self.remediation_note = self.root.get_by_label("Remediation note")
        self.remediate_button = self.root.get_by_role("button", name="Remediate")
        self.comment_box = self.root.get_by_label("Comment message")
        self.post_comment_button = self.root.get_by_role("button", name="Post comment")

    def wait_until_open(self) -> None:
        self.expect_visible(self.root, "alert details drawer is visible")

    def _select_from_single_select(self, trigger, option_label: str) -> None:
        self.select_custom_option(trigger, option_label, f"select {option_label}")

    def _expand_remediation_section_if_needed(self) -> None:
        if self.remediation_note.is_visible():
            return
        self.click(self.remediation_section_toggle, "expand remediation section")
        self.expect_visible(self.remediation_note, "remediation note input is visible")

    def change_status(self, status_label: str) -> None:
        with allure.step(f"Change alert status to {status_label}"):
            self._select_from_single_select(self.status_button, status_label)
            expect(self.status_button).to_contain_text(status_label)

    def assign_to(self, assignee_name: str) -> None:
        with allure.step(f"Assign alert to {assignee_name}"):
            self._select_from_single_select(self.assignee_button, assignee_name)
            expect(self.assignee_button).to_contain_text(assignee_name)

    def add_remediation_note(self, note: str) -> None:
        with allure.step("Add remediation note"):
            self._expand_remediation_section_if_needed()
            self.fill(self.remediation_note, note, "remediation note")

    def start_remediation(self) -> None:
        with allure.step("Start remediation"):
            self._expand_remediation_section_if_needed()
            self.click(self.remediate_button, "remediate button")

    def wait_for_status(self, status_label: str, timeout_ms: int = 180000) -> None:
        with allure.step(f"Wait for status {status_label}"):
            self.expect_text(
                self.status_button, status_label, f"alert status becomes {status_label}", timeout=timeout_ms
            )

    def add_comment(self, message: str) -> None:
        with allure.step("Add alert comment"):
            self.fill(self.comment_box, message, "comment message")
            self.click(self.post_comment_button, "post comment button")
            self.expect_visible(self.root.get_by_text(message), "new comment is visible")
