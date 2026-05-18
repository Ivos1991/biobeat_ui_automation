"""Reusable Playwright interaction primitives."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page, expect

from core.core_utils.logger import get_logger
from core.framework.hooks import StepContext, TestContext

if TYPE_CHECKING:
    from core.framework.runtime import FrameworkRuntime


class PlaywrightActions:
    """Composable UI actions with logging and framework step hooks."""

    def __init__(self, page: Page, *, runtime: FrameworkRuntime | None = None) -> None:
        self.page = page
        self.runtime = runtime
        self.logger = runtime.logger if runtime is not None else get_logger(self.__class__.__name__)

    def _emit_step(self, step_name: str, action: Callable[[], None]) -> None:
        test_context = None
        if self.runtime is not None:
            test_context = self.runtime.session_context.metadata.get("current_test")
            if isinstance(test_context, TestContext):
                self.runtime.hooks.emit("before_step", StepContext(test=test_context, step_name=step_name))
        try:
            action()
        finally:
            if self.runtime is not None and isinstance(test_context, TestContext):
                self.runtime.hooks.emit("after_step", StepContext(test=test_context, step_name=step_name))

    def fill(self, locator: Locator, value: str, description: str) -> None:
        self.logger.info("UI fill: %s", description)
        self._emit_step(description, lambda: locator.fill(value))

    def click(self, locator: Locator, description: str) -> None:
        self.logger.info("UI click: %s", description)
        self._emit_step(description, locator.click)

    def expect_visible(self, locator: Locator, description: str, timeout: int = 30000) -> None:
        self.logger.info("UI expect visible: %s", description)
        self._emit_step(description, lambda: expect(locator, description).to_be_visible(timeout=timeout))

    def expect_text(self, locator: Locator, text: str, description: str, timeout: int = 30000) -> None:
        self.logger.info("UI expect text: %s", description)
        self._emit_step(description, lambda: expect(locator, description).to_contain_text(text, timeout=timeout))

    def select_custom_option(self, trigger: Locator, option_label: str, description: str) -> None:
        self.logger.info("UI select option: %s -> %s", description, option_label)

        def action() -> None:
            trigger.click()
            option = self.page.get_by_role("option", name=option_label)
            expect(option, description).to_be_visible()
            option.click()

        self._emit_step(description, action)
