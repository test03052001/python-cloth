import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

LOG_FILE_NAME = "cloth_store.log"


def setup_logging() -> logging.Logger:
    """Configure a single rotating log file for app activity and exceptions."""
    log_dir = settings.log_path
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger("cloth_store")
    logger.setLevel(level)
    logger.handlers.clear()

    file_handler = RotatingFileHandler(
        log_dir / LOG_FILE_NAME,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger("cloth_store")
