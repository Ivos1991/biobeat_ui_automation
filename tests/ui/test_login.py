import allure
import pytest

from ui.pages.auth.login_page import LoginPage
from ui.pages.session_management.session_management_page import SessionManagementPage
from ui.pages.shell.app_shell_page import AppShellPage
from utils.assertions import assert_that


@pytest.mark.ui
@pytest.mark.smoke
def test_login_expects_user_can_authenticate_and_reach_session_management(page, page_factory, settings) -> None:
    """Verify that the configured BioBeat user can log in and land on Session Management."""
    login_page = page_factory.create(LoginPage, page)
    shell_page = page_factory.create(AppShellPage, page)
    session_page = page_factory.create(SessionManagementPage, page)

    with allure.step("Open the BioBeat login page"):
        login_page.open()
        login_page.wait_until_ready()

    with allure.step("Authenticate with the configured BioBeat user"):
        login_page.login(settings.username, settings.password)
        shell_page.wait_until_ready()
        session_page.wait_until_ready()

    with allure.step("Verify the user lands on Session Management after login"):
        assert_that(
            shell_page.session_management_button,
            "Session Management navigation button should be visible after login",
        ).is_visible()
        assert_that(
            session_page.search_session_input,
            "Session search input should be visible after login",
        ).is_visible()
        assert_that(
            session_page.current_url,
            "User should land on the Session Management route after login",
        ).contains("/session-management")
