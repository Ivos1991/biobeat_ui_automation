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
        """Apply the shared Playwright timeouts and keep access to runtime-level context."""
        self.page = page
        self.settings = settings
        self.runtime = runtime
        self.page.set_default_timeout(settings.timeouts.default_timeout_ms)
        self.page.set_default_navigation_timeout(settings.timeouts.navigation_timeout_ms)

    @property
    def current_url(self) -> str:
        """Expose the browser URL for route assertions in tests."""
        return self.page.url

    def goto(self, path: str) -> None:
        """Open an application-relative route and wait for initial loading to settle."""
        with allure.step(f"Open {path}"):
            self.page.goto(
                f"{self.settings.web_base_url.rstrip('/')}/{path.lstrip('/')}",
                wait_until="domcontentloaded",
            )
        self.wait_for_loading_to_finish()

    def wait_for_loading_to_finish(self) -> None:
        """Wait for the known BioBeat loader variants to stop being visible."""
        try:
            self.page.wait_for_function(
                """
                selectors => selectors.every(selector => {
                    const elements = Array.from(document.querySelectorAll(selector));
                    return elements.every(element => {
                        const style = window.getComputedStyle(element);
                        const rect = element.getBoundingClientRect();
                        const hiddenByStyle = style.display === "none" || style.visibility === "hidden";
                        const collapsed = rect.width === 0 && rect.height === 0;
                        return hiddenByStyle || collapsed;
                    });
                })
                """,
                arg=list(self._LOADER_SELECTORS),
                timeout=self.settings.timeouts.navigation_timeout_ms,
            )
        except Exception:
            # Some transitions do not render a loader. In that case the current DOM is already stable enough.
            return

    def wait_for_path(self, path_fragment: str) -> None:
        """Block until the browser path contains the requested route fragment."""
        self.page.wait_for_function(
            "pathFragment => window.location.pathname.includes(pathFragment)",
            arg=path_fragment,
            timeout=self.settings.timeouts.navigation_timeout_ms * 2,
        )
