"""Base class for Playwright page objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from config.settings import Settings

if TYPE_CHECKING:
    from core.framework.runtime import FrameworkRuntime


class BasePage:
    """Shared navigation and synchronization primitives for page objects."""

    _LOADER_SELECTORS: tuple[str, ...] = (
        "img[src*='Loader']",
        "img[src*='loader']",
        "img[src*='BBDarkLoader']",
    )

    def __init__(self, page: Page, settings: Settings, *, runtime: FrameworkRuntime | None = None) -> None:
        self.page = page
        self.settings = settings
        self.runtime = runtime
        self.page.set_default_timeout(settings.timeouts.default_timeout_ms)
        self.page.set_default_navigation_timeout(settings.timeouts.navigation_timeout_ms)

    @property
    def current_url(self) -> str:
        return self.page.url

    def goto(self, path: str) -> None:
        with allure.step(f"Open {path}"):
            self.page.goto(
                f"{self.settings.web_base_url.rstrip('/')}/{path.lstrip('/')}",
                wait_until="domcontentloaded",
            )
        self.wait_for_loading_to_finish()

    def wait_for_loading_to_finish(self, settle_ms: int = 400) -> None:
        self.page.wait_for_timeout(settle_ms)
        for selector in self._LOADER_SELECTORS:
            locator = self.page.locator(selector)
            try:
                if locator.count() > 0:
                    locator.last.wait_for(
                        state="hidden",
                        timeout=self.settings.timeouts.navigation_timeout_ms,
                    )
            except Exception:
                continue

    def wait_for_url(self, url_glob: str) -> None:
        self.page.wait_for_url(url_glob, timeout=self.settings.timeouts.navigation_timeout_ms * 2)
