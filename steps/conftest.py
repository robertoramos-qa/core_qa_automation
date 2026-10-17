"""Shared fixtures and step definitions available to all step files in this directory."""

import allure
import pytest
from playwright.sync_api import Page
from pytest_bdd import given, parsers, then, when

from helpers.logger_config import setup_logger
from pages.home_page import HomePage


logger = setup_logger("steps.conftest")


# ── Page Object, se deben instanciar todas las paginas que agregemos ───────────────────────────────────────────────────────

@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


# ── Given compartidos entre las paginas ─────────────────────────────────────────────────────────

@given("que el usuario abre la página principal de prometeo")
def open_homepage(home_page: HomePage, helper) -> None:
    logger.info("GIVEN: Abriendo página principal ")
    with allure.step("Navegar a https://prometeo-qa-demo.web.app/login"):
        home_page.open()
        helper.log_step("Página principal abierta")
        helper.take_screenshot("homepage_opened")


# ── Shared When Steps ──────────────────────────────────────────────────────────




# ── Shared Then Steps ──────────────────────────────────────────────────────────

