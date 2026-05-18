"""Administrative service operations."""

from assertpy import assert_that

from api.admin.admin_api import AdminApi
from api.admin.admin_response import ResetEnvironmentResponse
from core.core_utils.logger import get_logger
from core.framework.decorators import logged_call, retryable, timed_call


class AdminService:
    """Administrative operations used to prepare deterministic test state."""

    def __init__(self, admin_api: AdminApi) -> None:
        self.admin_api = admin_api
        self.logger = get_logger(self.__class__.__name__)

    @logged_call("Reset shared environment")
    @timed_call("admin.reset_environment")
    @retryable(3, (AssertionError,), delay_seconds=1.0)
    def reset_environment(self) -> ResetEnvironmentResponse:
        response = ResetEnvironmentResponse.from_dict(self.admin_api.reset_environment())
        assert_that(response.success).described_as("environment reset completed successfully").is_true()
        return response
