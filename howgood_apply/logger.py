"""Centralized application logger configuration."""

import sys

from loguru import logger

logger.remove()

logger.add(sys.stdout, format="{time} | {level} | {message} | {extra}", level="INFO")


def get_logger():
    """Return the configured Loguru logger instance."""
    return logger
