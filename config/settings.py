"""Strongly typed framework settings loaded from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from core.framework.types import Environment, EvidenceMode


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


@dataclass(slots=True)
class UrlSettings:
    web_base_url: str
    api_base_url: str


@dataclass(slots=True)
class CredentialsSettings:
    username: str
    password: str


@dataclass(slots=True)
class BrowserSettings:
    headless: bool
    slow_mo_ms: int
    ignore_https_errors: bool


@dataclass(slots=True)
class TimeoutSettings:
    request_timeout_seconds: float
    poll_timeout_seconds: float
    poll_interval_seconds: float


@dataclass(slots=True)
class RetrySettings:
    attempts: int
    delay_seconds: float


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
    """Strongly typed settings root for the automation framework."""

    urls: UrlSettings
    credentials: CredentialsSettings
    browser: BrowserSettings
    timeouts: TimeoutSettings
    retries: RetrySettings
    reporting: ReportingSettings
    plugins: PluginSettings
    runtime: RuntimeSettings

    @property
    def web_base_url(self) -> str:
        return self.urls.web_base_url

    @property
    def api_base_url(self) -> str:
        return self.urls.api_base_url

    @property
    def username(self) -> str:
        return self.credentials.username

    @property
    def password(self) -> str:
        return self.credentials.password

    @property
    def request_timeout_seconds(self) -> float:
        return self.timeouts.request_timeout_seconds

    @property
    def poll_timeout_seconds(self) -> float:
        return self.timeouts.poll_timeout_seconds

    @property
    def poll_interval_seconds(self) -> float:
        return self.timeouts.poll_interval_seconds

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
    def from_env(cls) -> "Settings":
        load_dotenv()
        artifact_dir = Path(os.getenv("ARTIFACT_DIR", "artifacts"))
        return cls(
            urls=UrlSettings(
                web_base_url=os.getenv("WEB_BASE_URL", "http://localhost:3000"),
                api_base_url=os.getenv("API_BASE_URL", "http://localhost:8080/api"),
            ),
            credentials=CredentialsSettings(
                username=os.getenv("APP_USERNAME", "admin"),
                password=os.getenv("APP_PASSWORD", "Aa123456"),
            ),
            browser=BrowserSettings(
                headless=_to_bool(os.getenv("HEADLESS"), True),
                slow_mo_ms=int(os.getenv("SLOW_MO_MS", "0")),
                ignore_https_errors=_to_bool(os.getenv("IGNORE_HTTPS_ERRORS"), True),
            ),
            timeouts=TimeoutSettings(
                request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")),
                poll_timeout_seconds=float(os.getenv("POLL_TIMEOUT_SECONDS", "180")),
                poll_interval_seconds=float(os.getenv("POLL_INTERVAL_SECONDS", "2")),
            ),
            retries=RetrySettings(
                attempts=int(os.getenv("RETRY_ATTEMPTS", "3")),
                delay_seconds=float(os.getenv("RETRY_DELAY_SECONDS", "1")),
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
