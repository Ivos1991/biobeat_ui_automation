"""Factories for creating runtime-aware page objects."""

from typing import TypeVar

from playwright.sync_api import Page

from config.settings import Settings
from core.framework.runtime import FrameworkRuntime
from ui.pages.base_page import BasePage


PageObjectT = TypeVar("PageObjectT", bound=BasePage)


class PageObjectFactory:
    """Creates page objects with shared configuration and runtime dependencies."""

    def __init__(self, settings: Settings, runtime: FrameworkRuntime) -> None:
        self.settings = settings
        self.runtime = runtime

    def create(self, page_type: type[PageObjectT], page: Page) -> PageObjectT:
        return page_type(page, self.settings, runtime=self.runtime)
