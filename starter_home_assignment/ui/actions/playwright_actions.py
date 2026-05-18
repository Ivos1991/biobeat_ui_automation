from playwright.sync_api import Locator, Page, expect

from core.core_utils.logger import get_logger


class PlaywrightActions:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def fill(self, locator: Locator, value: str, description: str) -> None:
        self.logger.info("UI fill: %s", description)
        locator.fill(value)

    def click(self, locator: Locator, description: str) -> None:
        self.logger.info("UI click: %s", description)
        locator.click()

    def expect_visible(self, locator: Locator, description: str, timeout: int = 30000) -> None:
        self.logger.info("UI expect visible: %s", description)
        expect(locator, description).to_be_visible(timeout=timeout)
