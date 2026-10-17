import configparser
import os

from helpers.logger_config import setup_logger

logger = setup_logger(__name__)


class Settings:
    """Singleton that loads test configuration from properties file + env vars.

    Priority order (highest first):
      1. Environment variables (TEST_BROWSER, TEST_HEADLESS)
      2. Properties file chosen by TEST_ENV (dev / qa / prod)
      3. Hard-coded defaults
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        env = os.environ.get("TEST_ENV", "qa").lower()
        props_path = os.path.join(
            os.path.dirname(__file__), "..", "properties", f"{env}.properties"
        )

        cfg = configparser.ConfigParser()
        cfg.read(props_path)

        self.env = env

        # URL
        self.base_url = cfg.get("environment", "base_url", fallback="")

        # Browser — env var overrides properties file
        browser_env = os.environ.get("TEST_BROWSER", "").strip().lower()
        self.browser = browser_env or cfg.get("browser", "name", fallback="chromium")

        # Headless — env var overrides properties file
        headless_env = os.environ.get("TEST_HEADLESS", "").strip().lower()
        if headless_env == "false":
            self.headless = False
        elif headless_env == "true":
            self.headless = True
        else:
            self.headless = cfg.getboolean("browser", "headless", fallback=True)

        self.slow_mo = cfg.getint("browser", "slow_mo", fallback=0)
        self.timeout = cfg.getint("browser", "timeout", fallback=30000)
        self.viewport_width = cfg.getint("browser", "viewport_width", fallback=1920)
        self.viewport_height = cfg.getint("browser", "viewport_height", fallback=1080)

        logger.info(
            f"Config: env={self.env} | url={self.base_url} | "
            f"browser={self.browser} | headless={self.headless}"
        )
