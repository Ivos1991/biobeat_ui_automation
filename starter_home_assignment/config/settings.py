import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    web_base_url: str
    api_base_url: str
    username: str
    password: str
    request_timeout_seconds: float
    poll_timeout_seconds: float
    poll_interval_seconds: float
    headless: bool
    slow_mo_ms: int
    browser_evidence_mode: str
    artifact_dir: Path
    log_level: str

    @property
    def log_dir(self) -> Path:
        return self.artifact_dir / "logs"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        artifact_dir = Path(os.getenv("ARTIFACT_DIR", "artifacts"))
        return cls(
            web_base_url=os.getenv("WEB_BASE_URL", "http://localhost:3000"),
            api_base_url=os.getenv("API_BASE_URL", "http://localhost:8080/api"),
            username=os.getenv("APP_USERNAME", "replace-me"),
            password=os.getenv("APP_PASSWORD", "replace-me"),
            request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")),
            poll_timeout_seconds=float(os.getenv("POLL_TIMEOUT_SECONDS", "60")),
            poll_interval_seconds=float(os.getenv("POLL_INTERVAL_SECONDS", "2")),
            headless=_to_bool(os.getenv("HEADLESS"), True),
            slow_mo_ms=int(os.getenv("SLOW_MO_MS", "0")),
            browser_evidence_mode=os.getenv("BROWSER_EVIDENCE_MODE", "on_failure").strip().lower(),
            artifact_dir=artifact_dir,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
