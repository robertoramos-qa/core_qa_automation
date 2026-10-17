import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

_LOG_FILE = None


def _get_log_file() -> str:
    global _LOG_FILE
    if _LOG_FILE is None:
        logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        session_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        _LOG_FILE = os.path.join(logs_dir, f"tests_{session_ts}.log")
    return _LOG_FILE


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        _get_log_file(),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
