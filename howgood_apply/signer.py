"""Create deterministic HMAC signatures for payloads."""

import hashlib
import hmac
import json


def sign(payload: dict[str, object], secret: str) -> str:
    """Return the HMAC-SHA256 signature for a JSON payload."""
    body = json.dumps(payload, separators=(",", ":"), default=str)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
