"""Unit tests for environment-based settings loading."""

import importlib
import sys

import pytest


def _reload_settings(monkeypatch: pytest.MonkeyPatch, **env: str | None):
    """Reload the settings module under a controlled environment."""
    for key in [
        "ENV",
        "DEV_HOWGOOD_SECRET",
        "DEV_HOWGOOD_ENDPOINT",
        "PROD_HOWGOOD_SECRET",
        "PROD_HOWGOOD_ENDPOINT",
    ]:
        monkeypatch.delenv(key, raising=False)

    for key, value in env.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)

    sys.modules.pop("howgood_apply.settings", None)
    return importlib.import_module("howgood_apply.settings")


def test_settings_loads_dev_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that dev values are loaded correctly."""
    settings = _reload_settings(
        monkeypatch,
        ENV="dev",
        DEV_HOWGOOD_SECRET="dev-secret",
        DEV_HOWGOOD_ENDPOINT="https://dev.example.com",
    )

    assert settings.SECRET == "dev-secret"
    assert settings.ENDPOINT == "https://dev.example.com"


def test_settings_loads_prod_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that prod values are loaded correctly."""
    settings = _reload_settings(
        monkeypatch,
        ENV="prod",
        PROD_HOWGOOD_SECRET="prod-secret",
        PROD_HOWGOOD_ENDPOINT="https://prod.example.com",
    )

    assert settings.SECRET == "prod-secret"
    assert settings.ENDPOINT == "https://prod.example.com"


def test_settings_raises_for_invalid_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that invalid ENV values raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid ENV"):
        _reload_settings(monkeypatch, ENV="staging")


def test_settings_raises_for_missing_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that a missing secret raises a ValueError."""
    with pytest.raises(ValueError, match="Missing HOWGOOD_SECRET"):
        _reload_settings(
            monkeypatch,
            ENV="dev",
            DEV_HOWGOOD_SECRET="",
            DEV_HOWGOOD_ENDPOINT="https://dev.example.com",
        )


def test_settings_raises_for_missing_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that a missing endpoint raises a ValueError."""
    with pytest.raises(ValueError, match="Missing HOWGOOD_ENDPOINT"):
        _reload_settings(
            monkeypatch,
            ENV="dev",
            DEV_HOWGOOD_SECRET="dev-secret",
            DEV_HOWGOOD_ENDPOINT="",
        )
