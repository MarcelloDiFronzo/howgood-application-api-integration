"""Unit tests for payload signing."""

import hashlib
import hmac
import json

from howgood_apply.signer import sign


def test_sign_returns_expected_hmac(dev_secret, sample_payload) -> None:
    """Verify that the signature matches the expected HMAC output."""
    expected_body = json.dumps(sample_payload, separators=(",", ":"), default=str)
    expected = hmac.new(
        dev_secret.encode(),
        expected_body.encode(),
        hashlib.sha256,
    ).hexdigest()

    assert sign(sample_payload, dev_secret) == expected


def test_sign_is_stable_for_same_input(dev_secret, sample_payload) -> None:
    """Verify that signing the same payload twice returns the same result."""
    assert sign(sample_payload, dev_secret) == sign(sample_payload, dev_secret)
