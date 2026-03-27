"""Unit tests for payload validation."""

import pytest

from howgood_apply.validator import validate


def test_validate_passes_with_all_required_fields() -> None:
    """Verify that a complete payload passes validation."""
    payload: dict[str, object] = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "resume": "https://example.com/resume.pdf",
        "location": "Remote",
        "linkedin": "https://linkedin.com/in/janedoe",
        "codeLink": "https://github.com/janedoe",
    }

    validate(payload)


@pytest.mark.parametrize(
    "payload, missing_fields",
    [
        ({}, ["name", "email", "resume", "location", "linkedin", "codeLink"]),
        ({"name": "Jane Doe"}, ["email", "resume", "location", "linkedin", "codeLink"]),
        (
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "resume": "https://example.com/resume.pdf",
                "location": "Remote",
                "linkedin": "https://linkedin.com/in/janedoe",
            },
            ["codeLink"],
        ),
        (
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "resume": "",
                "location": "Remote",
                "linkedin": "https://linkedin.com/in/janedoe",
                "codeLink": "https://github.com/janedoe",
            },
            ["resume"],
        ),
    ],
)
def test_validate_raises_on_missing_fields(
    payload: dict[str, object], missing_fields: list[str]
) -> None:
    """Verify that missing fields produce a helpful validation error."""
    with pytest.raises(ValueError, match=rf"Missing required fields: .*{missing_fields[0]}"):
        validate(payload)
