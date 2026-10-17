import os
from datetime import datetime

import allure
from playwright.sync_api import Page

from helpers.logger_config import setup_logger

logger = setup_logger(__name__)


class Helper:
    """Utility class for screenshot capture, error handling, and Allure reporting."""

    SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")

    def __init__(self, page: Page):
        self.page = page
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)

    # ── Screenshot ─────────────────────────────────────────────────────────────

    def take_screenshot(self, name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in name)
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.abspath(os.path.join(self.SCREENSHOTS_DIR, filename))

        try:
            self.page.screenshot(path=filepath, full_page=True)
            logger.info(f"Screenshot guardado: {filepath}")
            with open(filepath, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Screenshot: {name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            return filepath
        except Exception as exc:
            logger.error(f"Error al capturar screenshot '{name}': {exc}")
            return ""

    # ── Error handling ─────────────────────────────────────────────────────────

    def handle_error(self, error: Exception, context: str = "") -> None:
        logger.error(f"Error en '{context}': {type(error).__name__}: {error}")
        self.take_screenshot(f"ERROR_{context}")
        allure.attach(
            str(error),
            name=f"Error Details: {context}",
            attachment_type=allure.attachment_type.TEXT,
        )
        try:
            html_content = self.page.content()
            allure.attach(
                html_content,
                name="Page HTML at Error",
                attachment_type=allure.attachment_type.HTML,
            )
        except Exception:
            pass

    # ── Allure attachments ─────────────────────────────────────────────────────

    def log_step(self, step: str) -> None:
        logger.info(f"STEP: {step}")
        allure.attach(
            step,
            name="Step Info",
            attachment_type=allure.attachment_type.TEXT,
        )

    def attach_text(self, content: str, name: str) -> None:
        logger.debug(f"Adjuntando '{name}' al reporte")
        allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)

    def attach_html(self, content: str, name: str) -> None:
        allure.attach(content, name=name, attachment_type=allure.attachment_type.HTML)

    # ── Page interaction helpers ───────────────────────────────────────────────

    def wait_and_click(self, locator, timeout: int = 30000) -> None:
        logger.debug(f"Click: {locator}")
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()

    def wait_and_fill(self, locator, text: str, timeout: int = 30000) -> None:
        logger.debug(f"Fill: '{text}'")
        locator.wait_for(state="visible", timeout=timeout)
        locator.clear()
        locator.fill(text)

    def get_element_text(self, locator, timeout: int = 30000) -> str:
        locator.wait_for(state="visible", timeout=timeout)
        text = locator.inner_text()
        logger.debug(f"Texto obtenido: '{text}'")
        return text

    def is_element_visible(self, locator, timeout: int = 5000) -> bool:
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def scroll_to_element(self, locator) -> None:
        locator.scroll_into_view_if_needed()

    def get_current_url(self) -> str:
        url = self.page.url
        logger.debug(f"URL actual: {url}")
        return url

    def get_page_title(self) -> str:
        title = self.page.title()
        logger.debug(f"Título: '{title}'")
        return title
