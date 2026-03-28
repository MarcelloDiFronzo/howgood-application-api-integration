"""Load and validate the application payload from JSON files."""

import json
from pathlib import Path

from pydantic import BaseModel, HttpUrl


class Payload(BaseModel):
    """Schema for the application payload."""

    name: str
    email: str
    resume: HttpUrl
    location: str
    linkedin: HttpUrl
    codeLink: HttpUrl
    yearsPython: int = 0
    yearsDjango: int = 0
    repos: str | None = None
    notes: str | None = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_payload(path: str = "config/payload.json") -> dict:
    """Load a payload JSON file and return a validated dictionary."""
    file_path = Path(path)

    if not file_path.is_absolute():
        file_path = PROJECT_ROOT / file_path

    if not file_path.exists():
        raise FileNotFoundError(f"Payload file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    payload = Payload(**raw)
    return payload.model_dump()
