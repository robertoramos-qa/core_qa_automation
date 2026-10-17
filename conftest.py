"""Root conftest — Playwright configuration, session hooks, and screenshot-on-failure."""

import os
from datetime import datetime

import allure
import pytest

from config.settings import Settings
from helpers.helper import Helper
from helpers.logger_config import setup_logger

logger = setup_logger("conftest")
_settings = Settings()


# ── Session hooks ──────────────────────────────────────────────────────────────

def pytest_sessionstart(session) -> None:
    logger.info("=" * 60)
    logger.info("Playwright BDD Framework — Iniciando sesión")
    logger.info(f"  Ambiente  : {_settings.env.upper()}")
    logger.info(f"  URL       : {_settings.base_url}")
    logger.info(f"  Navegador : {_settings.browser}")
    logger.info(f"  Headless  : {_settings.headless}")
    logger.info("=" * 60)

    allure_dir = "allure-results"
    os.makedirs(allure_dir, exist_ok=True)
    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write(f"Environment={_settings.env.upper()}\n")
        f.write(f"Base.URL={_settings.base_url}\n")
        f.write(f"Browser={_settings.browser}\n")
        f.write(f"Headless={_settings.headless}\n")
        f.write(f"Execution.Date={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def pytest_sessionfinish(session, exitstatus) -> None:
    status = "PASSED" if exitstatus == 0 else "FAILED"
    logger.info("=" * 60)
    logger.info(f"Sesión finalizada — Estado: {status} (código {exitstatus})")
    logger.info("=" * 60)


# ── Playwright browser overrides ───────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_name():
    """Browser from properties file or TEST_BROWSER env var."""
    return _settings.browser


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "slow_mo": _settings.slow_mo,
        "headless": _settings.headless,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": _settings.viewport_width,
            "height": _settings.viewport_height,
        },
    }


# ── Helper fixture ─────────────────────────────────────────────────────────────

@pytest.fixture
def helper(page):
    return Helper(page)


# ── Automatic screenshot on test failure ───────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            _helper = Helper(page)
            screenshot_path = _helper.take_screenshot(f"FAILED_{item.name}")
            logger.error(f"Test FALLIDO: {item.name}")
            if report.longrepr:
                logger.error(f"Detalle: {str(report.longrepr)[:600]}")
