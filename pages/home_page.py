import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from helpers.logger_config import setup_logger

logger = setup_logger(__name__)


class HomePage(BasePage):
    """
    All selectors are kept here as class constants (Object Repository).
    """

    # ── Object Repository, todos los elementos de la pagina──────────────────────────────────────────────────────
    USER_INPUT = "#mat-input-0"
    PASSWORD_INPUT = "#mat-input-1"
    SIGN_IN_BUTTON = "button.status-primary"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Abrir la pagina") # para fines del reporteador debemos setear el allure step que se utiliza en esta pagina
    def open(self) -> None:
        logger.info("Abriendo página principal")
        self.navigate()

    @allure.step("Verificar que la página principal cargó")
    def is_loaded(self) -> bool:
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=self.settings.timeout)
            title = self.get_title()
            return "titulo pagina" in title.lower() or len(title) > 0
        except Exception as exc:
            logger.warning(f"Verificación de carga falló: {exc}")
            return False
    @allure.step("El usuario introduce credenciales {usr}{psw}")
    def introduce_cred(self, usr: str, psw: str) -> None:
        logger.info(f"Introduce credenciales")
        user = self.page.locator(self.USER_INPUT)
        psdw = self.page.locator(self.PASSWORD_INPUT)
        btn = self.page.locator(self.SIGN_IN_BUTTON)
        user.fill(usr)
        psdw.fill(psw)
        self.helper.wait_and_click(btn)



