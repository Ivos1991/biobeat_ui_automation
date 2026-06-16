from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import allure
from playwright.sync_api import Locator, expect


@dataclass(slots=True)
class AssertionBuilder:
    actual: Any
    description: str
    timeout_ms: int = 10_000

    def _locator(self) -> Locator:
        if not isinstance(self.actual, Locator):
            raise TypeError(f"{self.description}: expected a Playwright Locator assertion target.")
        return self.actual

    def is_visible(self) -> AssertionBuilder:
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_visible(timeout=self.timeout_ms)
        return self

    def is_hidden(self) -> AssertionBuilder:
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_hidden(timeout=self.timeout_ms)
        return self

    def is_enabled(self) -> AssertionBuilder:
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_enabled(timeout=self.timeout_ms)
        return self

    def is_disabled(self) -> AssertionBuilder:
        with allure.step(self.description):
            expect(self._locator(), self.description).to_be_disabled(timeout=self.timeout_ms)
        return self

    def contains_text(self, expected: str) -> AssertionBuilder:
        with allure.step(self.description):
            expect(self._locator(), self.description).to_contain_text(expected, timeout=self.timeout_ms)
        return self

    def is_equal_to(self, expected: Any) -> AssertionBuilder:
        with allure.step(self.description):
            if self.actual != expected:
                raise AssertionError(f"{self.description}: expected {expected!r}, got {self.actual!r}.")
        return self

    def contains(self, expected: Any) -> AssertionBuilder:
        with allure.step(self.description):
            if expected not in self.actual:
                raise AssertionError(
                    f"{self.description}: expected to contain {expected!r}, got {self.actual!r}."
                )
        return self

    def is_true(self) -> AssertionBuilder:
        return self.is_equal_to(True)

    def is_false(self) -> AssertionBuilder:
        return self.is_equal_to(False)

    def is_not_none(self) -> AssertionBuilder:
        with allure.step(self.description):
            if self.actual is None:
                raise AssertionError(f"{self.description}: expected a non-null value.")
        return self


def assert_that(actual: Any, description: str, *, timeout_ms: int = 10_000) -> AssertionBuilder:
    return AssertionBuilder(actual=actual, description=description, timeout_ms=timeout_ms)
