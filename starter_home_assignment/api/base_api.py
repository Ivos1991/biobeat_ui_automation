from typing import Iterable

import requests
from requests import Response

from config.settings import Settings
from core.core_utils.logger import get_logger
from core.exceptions import ApiRequestError
from core.reporting import attach_json, attach_text


class BaseApi:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_url = settings.api_base_url.rstrip("/")
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)
        self._token: str | None = None

    def set_token(self, token: str) -> None:
        self._token = token

    def execute(self, method: str, path: str, *, expected_status: int | Iterable[int] = 200, **kwargs) -> Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = dict(kwargs.pop("headers", {}))
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        kwargs.setdefault("timeout", self.settings.request_timeout_seconds)

        self.logger.info("API %s %s", method.upper(), url)
        response = self.session.request(method=method.upper(), url=url, headers=headers, **kwargs)
        self.logger.info("API %s %s -> %s", method.upper(), url, response.status_code)

        allowed = {expected_status} if isinstance(expected_status, int) else set(expected_status)
        if response.status_code not in allowed:
            attach_text("api-error-url", url)
            attach_text("api-error-response", response.text)
            raise ApiRequestError(
                message=f"Unexpected status {response.status_code} for {method.upper()} {url}",
                status_code=response.status_code,
                response_text=response.text,
            )
        return response

    def execute_json(self, method: str, path: str, *, expected_status: int | Iterable[int] = 200, attach_name: str | None = None, **kwargs) -> dict | list | None:
        response = self.execute(method, path, expected_status=expected_status, **kwargs)
        if response.status_code == 204 or not response.content:
            return None

        payload = response.json()
        if attach_name:
            if isinstance(payload, dict):
                attach_json(attach_name, payload)
            else:
                attach_text(attach_name, str(payload))
        return payload
