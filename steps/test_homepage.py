"""BDD test runner for homepage.feature — homepage-specific step definitions."""

import allure
import pytest
from pytest_bdd import parsers, scenarios, then, when

from helpers.logger_config import setup_logger
from pages.home_page import HomePage

logger = setup_logger(__name__)

scenarios("homepage.feature")


# ── Then Steps — pasos especificos para Homepage  ────────────────────────────────────────────

@then("la página principal debe estar cargada")
def verify_homepage_loaded(home_page: HomePage, helper) -> None:
    logger.info("THEN: Verificando que la página principal cargó")
    with allure.step("Verificar carga de la página principal"): #para fines del reporteador se debe parametrizar
        assert home_page.is_loaded(), "La página principal no cargó correctamente"
        helper.take_screenshot("homepage_loaded_verified")


@then(parsers.parse('el título de la página debe contener "{expected_title}"'))
def verify_homepage_title_contains(home_page: HomePage, expected_title: str) -> None:
    logger.info(f"THEN: Verificando que el título contiene '{expected_title}'")
    with allure.step(f"Verificar título: contiene '{expected_title}'"):
        actual_title = home_page.get_title()
        assert expected_title.lower() in actual_title.lower(), (
            f"Título esperado que contenga: '{expected_title}', Título actual: '{actual_title}'"
        )
@when(parsers.parse('el usuario introduce usuario "{user}" y contraseña "{password}"'))
def loging_homepage(home_page: HomePage, helper, user: str, password: str) -> None:
    logger.info(f"WHEN: el usuario introduce credenciales ")
    with allure.step(f"El usuario introduce credenciales {user} {password}"):
        home_page.introduce_cred(user,password)
        helper.take_screenshot("homepage_loaded_verified")