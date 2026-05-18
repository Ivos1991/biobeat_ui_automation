"""Base API client with lifecycle hooks and shared request behavior."""

import json
from time import perf_counter
from typing import TYPE_CHECKING, Iterable

import requests
from requests import Response, Session

from config.settings import Settings
from core.core_utils.logger import get_logger
from core.exceptions import ApiRequestError
from core.framework.hooks import ApiCallContext
from core.reporting import attach_json, attach_text

if TYPE_CHECKING:
    from core.framework.runtime import FrameworkRuntime


class BaseApi:
    """Base HTTP client that centralizes authentication, hooks, and errors."""

    def __init__(self, settings: Settings, *, runtime: "FrameworkRuntime" | None = None, session: Session | None = None) -> None:
        self.settings = settings
        self.runtime = runtime
        self.base_url = settings.api_base_url.rstrip("/")
        self.session = session or requests.Session()
        self.logger = runtime.logger if runtime is not None else get_logger(self.__class__.__name__)
        self._token: str | None = None

    def set_token(self, token: str) -> None:
        self._token = token

    def execute(self, method: str, path: str, *, expected_status: int | Iterable[int] = 200, **kwargs) -> Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = dict(kwargs.pop("headers", {}))
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        kwargs.setdefault("timeout", self.settings.request_timeout_seconds)

        allowed = (expected_status,) if isinstance(expected_status, int) else tuple(expected_status)
        context = ApiCallContext(
            client_name=self.__class__.__name__,
            method=method.upper(),
            url=url,
            expected_statuses=allowed,
            request_kwargs={"timeout": kwargs.get("timeout")},
        )
        if self.runtime is not None:
            self.runtime.hooks.emit("before_api_call", context)

        self.logger.info("API %s %s", method.upper(), url)
        started = perf_counter()
        response: Response | None = None
        try:
            response = self.session.request(method=method.upper(), url=url, headers=headers, **kwargs)
            context.status_code = response.status_code
            return response
        except Exception as error:
            context.error = error
            raise
        finally:
            if response is not None and response.content:
                try:
                    context.response_payload = response.json()
                except ValueError:
                    context.response_payload = response.text
            context.duration_ms = (perf_counter() - started) * 1000
            if self.runtime is not None:
                self.runtime.hooks.emit("after_api_call", context)

    def execute_json(self, method: str, path: str, *, expected_status: int | Iterable[int] = 200, attach_name: str | None = None, **kwargs) -> dict | list | None:
        response = self.execute(method, path, expected_status=expected_status, **kwargs)
        self.logger.info("API %s %s -> %s", method.upper(), response.url, response.status_code)

        allowed = {expected_status} if isinstance(expected_status, int) else set(expected_status)
        if response.status_code not in allowed:
            attach_text("api-error-url", response.url)
            attach_text("api-error-response", response.text)
            raise ApiRequestError(
                message=f"Unexpected status {response.status_code} for {method.upper()} {response.url}",
                status_code=response.status_code,
                response_text=response.text,
            )

        if response.status_code == 204 or not response.content:
            return None

        payload = response.json()
        if attach_name:
            if isinstance(payload, dict):
                attach_json(attach_name, payload)
            else:
                attach_text(attach_name, json.dumps(payload, indent=2))
        return payload
