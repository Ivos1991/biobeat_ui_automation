"""Typed framework settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from core.framework.types import BrowserName, Environment, EvidenceMode


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _csv(value: str | None, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    return tuple(item.strip() for item in value.split(",") if item.strip()) or default


def _resolve_evidence_mode(value: str | None) -> EvidenceMode:
    raw = (value or "failure_only").strip().lower()
    aliases = {
        "on_failure": "failure_only",
        "always": "full_evidence",
        "off": "off",
        "failure_only": "failure_only",
        "full_evidence": "full_evidence",
    }
    try:
        return aliases[raw]  # type: ignore[return-value]
    except KeyError as error:
        raise ValueError(
            "BROWSER_EVIDENCE_MODE must be one of: off, on_failure, always, failure_only, full_evidence"
        ) from error


def _resolve_browser_name(value: str | None) -> BrowserName:
    raw = (value or "chromium").strip().lower()
    allowed: set[str] = {"chromium", "firefox", "webkit"}
    if raw not in allowed:
        raise ValueError("BROWSER must be one of: chromium, firefox, webkit")
    return raw  # type: ignore[return-value]


@dataclass(slots=True)
class UrlSettings:
    web_base_url: str
    login_path: str


@dataclass(slots=True)
class CredentialsSettings:
    username: str
    password: str

    @property
    def is_configured(self) -> bool:
        return bool(self.username and self.password)


@dataclass(slots=True)
class BrowserSettings:
    browser_name: BrowserName
    headless: bool
    slow_mo_ms: int
    ignore_https_errors: bool


@dataclass(slots=True)
class TimeoutSettings:
    default_timeout_ms: int
    expect_timeout_ms: int
    navigation_timeout_ms: int


@dataclass(slots=True)
class ReportingSettings:
    evidence_mode: EvidenceMode
    artifact_dir: Path

    @property
    def allure_results_dir(self) -> Path:
        return self.artifact_dir / "allure-results"

    @property
    def log_dir(self) -> Path:
        return self.artifact_dir / "logs"

    @property
    def allure_report_dir(self) -> Path:
        return self.artifact_dir / "allure-report"

    @property
    def playwright_output_dir(self) -> Path:
        return self.artifact_dir / "playwright"


@dataclass(slots=True)
class PluginSettings:
    enabled: tuple[str, ...]


@dataclass(slots=True)
class RuntimeSettings:
    environment: Environment
    log_level: str


@dataclass(slots=True)
class Settings:
    urls: UrlSettings
    credentials: CredentialsSettings
    browser: BrowserSettings
    timeouts: TimeoutSettings
    reporting: ReportingSettings
    plugins: PluginSettings
    runtime: RuntimeSettings

    @property
    def web_base_url(self) -> str:
        return self.urls.web_base_url

    @property
    def login_path(self) -> str:
        return self.urls.login_path

    @property
    def username(self) -> str:
        return self.credentials.username

    @property
    def password(self) -> str:
        return self.credentials.password

    @property
    def has_app_credentials(self) -> bool:
        return self.credentials.is_configured

    @property
    def browser_name(self) -> BrowserName:
        return self.browser.browser_name

    @property
    def headless(self) -> bool:
        return self.browser.headless

    @property
    def slow_mo_ms(self) -> int:
        return self.browser.slow_mo_ms

    @property
    def browser_evidence_mode(self) -> EvidenceMode:
        return self.reporting.evidence_mode

    @property
    def artifact_dir(self) -> Path:
        return self.reporting.artifact_dir

    @property
    def allure_results_dir(self) -> Path:
        return self.reporting.allure_results_dir

    @property
    def log_dir(self) -> Path:
        return self.reporting.log_dir

    @property
    def allure_report_dir(self) -> Path:
        return self.reporting.allure_report_dir

    @property
    def playwright_output_dir(self) -> Path:
        return self.reporting.playwright_output_dir

    @property
    def log_level(self) -> str:
        return self.runtime.log_level

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        artifact_dir = Path(os.getenv("ARTIFACT_DIR", "artifacts"))
        return cls(
            urls=UrlSettings(
                web_base_url=os.getenv("WEB_BASE_URL", "https://bpm-demo.eu.bio-beat.cloud").rstrip("/"),
                login_path=os.getenv("LOGIN_PATH", "/login"),
            ),
            credentials=CredentialsSettings(
                username=(os.getenv("APP_USERNAME") or os.getenv("BIOBEAT_USERNAME") or "").strip(),
                password=(os.getenv("APP_PASSWORD") or os.getenv("BIOBEAT_PASSWORD") or "").strip(),
            ),
            browser=BrowserSettings(
                browser_name=_resolve_browser_name(os.getenv("BROWSER")),
                headless=_to_bool(os.getenv("HEADLESS"), True),
                slow_mo_ms=int(os.getenv("SLOW_MO_MS", "0")),
                ignore_https_errors=_to_bool(os.getenv("IGNORE_HTTPS_ERRORS"), True),
            ),
            timeouts=TimeoutSettings(
                default_timeout_ms=int(os.getenv("DEFAULT_TIMEOUT_MS", "15000")),
                expect_timeout_ms=int(os.getenv("EXPECT_TIMEOUT_MS", "10000")),
                navigation_timeout_ms=int(os.getenv("NAVIGATION_TIMEOUT_MS", "30000")),
            ),
            reporting=ReportingSettings(
                evidence_mode=_resolve_evidence_mode(os.getenv("BROWSER_EVIDENCE_MODE")),
                artifact_dir=artifact_dir,
            ),
            plugins=PluginSettings(enabled=_csv(os.getenv("ENABLED_PLUGINS"), ("session_logger", "allure_evidence"))),
            runtime=RuntimeSettings(
                environment=Environment(os.getenv("FRAMEWORK_ENV", "local").strip().lower()),
                log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            ),
        )
