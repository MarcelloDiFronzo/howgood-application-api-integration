"""Unit tests for payload loading and validation."""

import json
from pathlib import Path

import pytest

import howgood_apply.config_loader as config_loader


def test_load_payload_reads_and_validates_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that a valid payload file is loaded and normalized."""
    payload_file = tmp_path / "payload.json"
    payload_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "resume": "https://example.com/resume.pdf",
        "location": "Remote",
        "linkedin": "https://linkedin.com/in/janedoe",
        "codeLink": "https://github.com/janedoe",
        "yearsPython": 7,
        "yearsDjango": 3,
        "repos": "https://github.com/janedoe?tab=repositories",
        "notes": "Great candidate",
    }
    payload_file.write_text(json.dumps(payload_data), encoding="utf-8")

    monkeypatch.setattr(config_loader, "PROJECT_ROOT", tmp_path)

    result = config_loader.load_payload("payload.json")

    assert result["name"] == payload_data["name"]
    assert result["email"] == payload_data["email"]
    assert str(result["resume"]) == payload_data["resume"]
    assert result["location"] == payload_data["location"]
    assert str(result["linkedin"]) == payload_data["linkedin"]
    assert str(result["codeLink"]) == payload_data["codeLink"]
    assert result["yearsPython"] == payload_data["yearsPython"]
    assert result["yearsDjango"] == payload_data["yearsDjango"]
    assert result["repos"] == payload_data["repos"]
    assert result["notes"] == payload_data["notes"]


def test_load_payload_raises_for_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that missing payload files raise FileNotFoundError."""
    monkeypatch.setattr(config_loader, "PROJECT_ROOT", tmp_path)

    with pytest.raises(FileNotFoundError, match="Payload file not found:"):
        config_loader.load_payload("missing.json")


def test_load_payload_accepts_absolute_path(tmp_path: Path) -> None:
    """Verify that absolute paths are handled without PROJECT_ROOT resolution."""
    payload_file = tmp_path / "payload.json"
    payload_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "resume": "https://example.com/resume.pdf",
        "location": "Remote",
        "linkedin": "https://linkedin.com/in/janedoe",
        "codeLink": "https://github.com/janedoe",
    }
    payload_file.write_text(json.dumps(payload_data), encoding="utf-8")

    result = config_loader.load_payload(str(payload_file))

    assert result["name"] == payload_data["name"]
    assert result["email"] == payload_data["email"]
    assert str(result["resume"]) == payload_data["resume"]
    assert result["location"] == payload_data["location"]
    assert str(result["linkedin"]) == payload_data["linkedin"]
    assert str(result["codeLink"]) == payload_data["codeLink"]
