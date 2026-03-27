"""Unit tests for the top-level application entry point."""

import importlib
from unittest.mock import MagicMock

import pytest


def test_main_success(monkeypatch: pytest.MonkeyPatch, dev_secret, dev_endpoint) -> None:
    """Verify that the main function loads and submits the payload successfully."""
    apply_module = importlib.import_module("apply")

    load_payload_mock = MagicMock(return_value={"name": "Jane"})
    submit_mock = MagicMock(return_value={"status": "ok"})
    info_mock = MagicMock()
    error_mock = MagicMock()

    monkeypatch.setattr(apply_module, "load_payload", load_payload_mock)
    monkeypatch.setattr(apply_module, "submit", submit_mock)
    monkeypatch.setattr(apply_module.logger, "info", info_mock)
    monkeypatch.setattr(apply_module.logger, "error", error_mock)

    apply_module.main()

    load_payload_mock.assert_called_once_with()
    submit_mock.assert_called_once_with(
        {"name": "Jane"},
        apply_module.ENDPOINT,
        apply_module.SECRET,
    )
    error_mock.assert_not_called()


def test_main_logs_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that failures are logged with the exception message."""
    apply_module = importlib.import_module("apply")

    load_payload_mock = MagicMock(side_effect=ValueError("boom"))
    info_mock = MagicMock()
    error_mock = MagicMock()

    monkeypatch.setattr(apply_module, "load_payload", load_payload_mock)
    monkeypatch.setattr(apply_module.logger, "info", info_mock)
    monkeypatch.setattr(apply_module.logger, "error", error_mock)

    apply_module.main()

    error_mock.assert_called_once_with("Submission failed", error="boom")
