"""Validate that the payload contains the required fields."""

REQUIRED_FIELDS = ["name", "email", "resume", "location", "linkedin", "codeLink"]


def validate(payload: dict[str, object]) -> None:
    """Raise an error if required payload fields are missing."""
    missing = [f for f in REQUIRED_FIELDS if not payload.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
