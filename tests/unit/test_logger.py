"""Unit tests for logger configuration."""

from howgood_apply.logger import get_logger, logger


def test_get_logger_returns_same_logger_instance() -> None:
    """Verify that get_logger returns the configured singleton logger."""
    assert get_logger() is logger
