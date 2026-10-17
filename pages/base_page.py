import allure
from playwright.sync_api import Page

from config.settings import Settings
from helpers.helper import Helper
from helpers.logger_config import setup_logger

logger = setup_logger(__name__)


class BasePage:
    """Base class for all Page Objects. Provides navigation, title, and helper access."""

    def __init__(self, page: Page):
        self.page = page
        self.settings = Settings()
        self.helper = Helper(page)

    @allure.step("Navegar a {path}")
    def navigate(self, path: str = "") -> None:
        url = f"{self.settings.base_url}{path}"
        logger.info(f"Navegando a: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded", timeout=self.settings.timeout)

    def get_title(self) -> str:
        return self.helper.get_page_title()

    def get_url(self) -> str:
        return self.helper.get_current_url()

    def take_screenshot(self, name: str) -> str:
        return self.helper.take_screenshot(name)

    def wait_for_network_idle(self) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=self.settings.timeout)
        except Exception:
            logger.warning("networkidle timeout — continuando de todos modos")
