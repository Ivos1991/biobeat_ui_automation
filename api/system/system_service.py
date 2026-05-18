"""System service layer."""

from assertpy import assert_that

from api.system.system_api import SystemApi
from api.system.system_response import HealthResponse
from core.core_utils.logger import get_logger
from core.framework.decorators import logged_call, timed_call


class SystemService:
    """Read-only service for platform health and configuration endpoints."""

    def __init__(self, system_api: SystemApi) -> None:
        self.system_api = system_api
        self.logger = get_logger(self.__class__.__name__)

    @logged_call("Check platform health")
    @timed_call("system.health")
    def health(self) -> HealthResponse:
        response = HealthResponse.from_dict(self.system_api.health())
        assert_that(response.data).described_as("health response should not be empty").is_not_empty()
        return response

    @logged_call("Fetch policy configuration")
    @timed_call("system.policy_config")
    def policy_config(self) -> dict:
        response = self.system_api.policy_config()
        assert_that(response).described_as("policy config response should not be empty").is_not_empty()
        return response
