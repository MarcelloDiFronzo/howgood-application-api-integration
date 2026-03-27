"""Unit tests for payload signing."""

import hashlib
import hmac
import json

from howgood_apply.signer import sign


def test_sign_returns_expected_hmac(dev_secret) -> None:
    """Verify that the signature matches the expected HMAC output."""
    payload = {"name": "Jane Doe", "yearsPython": 5}

    expected_body = json.dumps(payload, separators=(",", ":"), default=str)
    expected = hmac.new(
        dev_secret.encode(),
        expected_body.encode(),
        hashlib.sha256,
    ).hexdigest()

    assert sign(payload, dev_secret) == expected


def test_sign_is_stable_for_same_input(dev_secret) -> None:
    """Verify that signing the same payload twice returns the same result."""
    payload = {"a": 1, "b": "two"}

    assert sign(payload, dev_secret) == sign(payload, dev_secret)
