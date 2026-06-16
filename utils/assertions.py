from typing import Any, Self

import allure
from playwright.sync_api import Locator, expect


class AssertionBuilder:
    """Wrap Playwright and value assertions behind a consistent fluent API for tests."""
    __slots__ = ("actual", "description", "timeout_ms")

    def __init__(self, actual: Any, description: str, timeout_ms: int = 10_000) -> None:
        """Store the assertion target together with its review-friendly description."""
        self.actual = actual
        self.description = description
        self.timeout_ms = timeout_ms

    def _locator(self) -> Locator:
        """Validate that a locator-based assertion received a Playwright Locator target."""
        if not isinstance(self.actual, Locator):
            raise TypeError(f"{self.description}: expected a Playwright Locator assertion target.")
        return self.actual

    def is_visible(self) -> Self:
        """Assert that a locator is visible to the user."""
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_visible(timeout=self.timeout_ms)
        return self

    def is_hidden(self) -> Self:
        """Assert that a locator is hidden from the user."""
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_hidden(timeout=self.timeout_ms)
        return self

    def is_enabled(self) -> Self:
        """Assert that a locator is enabled for interaction."""
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_enabled(timeout=self.timeout_ms)
        return self

    def is_disabled(self) -> Self:
        """Assert that a locator is disabled for interaction."""
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_disabled(timeout=self.timeout_ms)
        return self

    def contains_text(self, expected: str) -> Self:
        """Assert that a locator contains the expected user-facing text."""
        with allure.step(self.description):
            expect(self._locator(), self.description).to_contain_text(expected, timeout=self.timeout_ms)
        return self

    def is_equal_to(self, expected: Any) -> Self:
        """Assert value equality for non-locator results."""
        with allure.step(self.description):
            if self.actual != expected:
                raise AssertionError(f"{self.description}: expected {expected!r}, got {self.actual!r}.")
        return self

    def contains(self, expected: Any) -> Self:
        """Assert that a collection or string contains the expected value."""
        with allure.step(self.description):
            if expected not in self.actual:
                raise AssertionError(
                    f"{self.description}: expected to contain {expected!r}, got {self.actual!r}."
                )
        return self

    def is_true(self) -> Self:
        """Assert that the current value is exactly True."""
        return self.is_equal_to(True)

    def is_false(self) -> Self:
        """Assert that the current value is exactly False."""
        return self.is_equal_to(False)

    def is_not_none(self) -> Self:
        """Assert that the current value is not None."""
        with allure.step(self.description):
            if self.actual is None:
                raise AssertionError(f"{self.description}: expected a non-null value.")
        return self


def assert_that(actual: Any, description: str, *, timeout_ms: int = 10_000) -> AssertionBuilder:
    """Create a fluent assertion wrapper with a review-friendly description."""
    return AssertionBuilder(actual=actual, description=description, timeout_ms=timeout_ms)
