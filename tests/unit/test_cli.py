"""Unit tests for the CLI entry point."""

import argparse
from unittest.mock import MagicMock

import pytest

import howgood_apply.cli as cli


def test_main_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that CLI arguments are parsed and submitted correctly."""
    args = MagicMock()
    args.config = "custom.json"

    parse_args_mock: MagicMock = MagicMock(return_value=args)
    load_payload_mock: MagicMock = MagicMock(return_value={"name": "Jane"})
    submit_mock: MagicMock = MagicMock(return_value={"status": "ok"})
    info_mock: MagicMock = MagicMock()
    error_mock: MagicMock = MagicMock()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", parse_args_mock)
    monkeypatch.setattr(cli, "load_payload", load_payload_mock)
    monkeypatch.setattr(cli, "submit", submit_mock)
    monkeypatch.setattr(cli.logger, "info", info_mock)
    monkeypatch.setattr(cli.logger, "error", error_mock)

    cli.main()

    load_payload_mock.assert_called_once_with("custom.json")
    submit_mock.assert_called_once_with({"name": "Jane"}, cli.ENDPOINT, cli.SECRET)
    error_mock.assert_not_called()


def test_main_logs_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that CLI failures are logged."""
    args = MagicMock()
    args.config = "bad.json"

    parse_args_mock: MagicMock = MagicMock(return_value=args)
    load_payload_mock: MagicMock = MagicMock(side_effect=ValueError("boom"))
    info_mock: MagicMock = MagicMock()
    error_mock: MagicMock = MagicMock()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", parse_args_mock)
    monkeypatch.setattr(cli, "load_payload", load_payload_mock)
    monkeypatch.setattr(cli.logger, "info", info_mock)
    monkeypatch.setattr(cli.logger, "error", error_mock)

    cli.main()

    error_mock.assert_called_once_with("Submission failed", error="boom")
