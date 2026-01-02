"""
logger.py

Centralized logging configuration for the SOQL Agent.
Safe for production and GitHub (no secrets logged).
"""

import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOG_FORMAT = (
    "[%(asctime)s] "
    "[%(levelname)s] "
    "[%(name)s] "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _configure_logger() -> logging.Logger:
    logger = logging.getLogger("soql-agent")

    if logger.handlers:
        return logger  # Prevent duplicate handlers in Streamlit / reloads

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = _configure_logger()
