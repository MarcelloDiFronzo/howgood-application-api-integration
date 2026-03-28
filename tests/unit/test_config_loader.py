"""Unit tests for payload loading and validation."""

import json
from pathlib import Path

import pytest

import howgood_apply.config_loader as config_loader


def test_load_payload_reads_and_validates_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, sample_payload
) -> None:
    """Verify that a valid payload file is loaded and normalized."""
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps(sample_payload), encoding="utf-8")

    monkeypatch.setattr(config_loader, "PROJECT_ROOT", tmp_path)

    result = config_loader.load_payload("payload.json")

    assert result["name"] == sample_payload["name"]
    assert result["email"] == sample_payload["email"]
    assert str(result["resume"]) == sample_payload["resume"]
    assert result["location"] == sample_payload["location"]
    assert str(result["linkedin"]) == sample_payload["linkedin"]
    assert str(result["codeLink"]) == sample_payload["codeLink"]
    assert result["yearsPython"] == sample_payload["yearsPython"]
    assert result["yearsDjango"] == sample_payload["yearsDjango"]
    assert result["repos"] == sample_payload["repos"]
    assert result["notes"] == sample_payload["notes"]


def test_load_payload_raises_for_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that missing payload files raise FileNotFoundError."""
    monkeypatch.setattr(config_loader, "PROJECT_ROOT", tmp_path)

    with pytest.raises(FileNotFoundError, match="Payload file not found:"):
        config_loader.load_payload("missing.json")


def test_load_payload_accepts_absolute_path(tmp_path: Path, sample_payload) -> None:
    """Verify that absolute paths are handled without PROJECT_ROOT resolution."""
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps(sample_payload), encoding="utf-8")

    result = config_loader.load_payload(str(payload_file))

    assert result["name"] == sample_payload["name"]
    assert result["email"] == sample_payload["email"]
    assert str(result["resume"]) == sample_payload["resume"]
    assert result["location"] == sample_payload["location"]
    assert str(result["linkedin"]) == sample_payload["linkedin"]
    assert str(result["codeLink"]) == sample_payload["codeLink"]
