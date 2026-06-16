"""Factories for creating runtime-aware page objects."""

from typing import TypeVar

from playwright.sync_api import Page

from config.settings import Settings
from core.framework.runtime import FrameworkRuntime
from ui.pages.base_page import BasePage

PageObjectT = TypeVar("PageObjectT", bound=BasePage)


class PageObjectFactory:
    """Creates page objects with the shared dependencies already wired in.

    This keeps page-object construction consistent across flows and fixtures by
    injecting the current Playwright page together with the framework settings
    and runtime.
    """

    def __init__(self, settings: Settings, runtime: FrameworkRuntime) -> None:
        """Persist the shared objects injected into every page object."""
        self.settings = settings
        self.runtime = runtime

    def create(self, page_type: type[PageObjectT], page: Page) -> PageObjectT:
        """Instantiate a page object with the active Playwright page and framework context."""
        return page_type(page, self.settings, runtime=self.runtime)
