"""Unit tests for the HTTP submission client."""

import json
from unittest.mock import MagicMock

import pytest
import requests

import howgood_apply.client as client


def test_submit_success(
    monkeypatch: pytest.MonkeyPatch, dev_secret, dev_endpoint, sample_payload
) -> None:
    """Verify a successful request returns the decoded JSON response."""
    response: MagicMock = MagicMock()
    response.status_code = 200
    response.json.return_value = {"ok": True}
    response.raise_for_status.return_value = None

    post_mock: MagicMock = MagicMock(return_value=response)
    time_mock: MagicMock = MagicMock()
    validate_mock: MagicMock = MagicMock()
    sign_mock: MagicMock = MagicMock(return_value="signature-123")
    info_mock: MagicMock = MagicMock()
    error_mock: MagicMock = MagicMock()

    time_mock.time.side_effect = [100.0, 100.25]
    time_mock.sleep = MagicMock()

    monkeypatch.setattr(client.requests, "post", post_mock)
    monkeypatch.setattr(client, "time", time_mock)
    monkeypatch.setattr(client, "validate", validate_mock)
    monkeypatch.setattr(client, "sign", sign_mock)
    monkeypatch.setattr(client.logger, "info", info_mock)
    monkeypatch.setattr(client.logger, "error", error_mock)

    result = client.submit(sample_payload, dev_endpoint, dev_secret, retries=1)

    assert result == {"ok": True}
    validate_mock.assert_called_once_with(sample_payload)
    sign_mock.assert_called_once_with(sample_payload, dev_secret)
    post_mock.assert_called_once_with(
        dev_endpoint,
        data=json.dumps(sample_payload, separators=(",", ":"), default=str),
        headers={
            "Content-Type": "application/json",
            "X-HMAC-Signature": "signature-123",
        },
        timeout=10,
    )
    error_mock.assert_not_called()


def test_submit_retries_then_succeeds(
    monkeypatch: pytest.MonkeyPatch, dev_secret, dev_endpoint, sample_payload
) -> None:
    """Verify that transient failures are retried and then succeed."""
    response: MagicMock = MagicMock()
    response.status_code = 200
    response.json.return_value = {"ok": True}
    response.raise_for_status.return_value = None

    first_exc = requests.exceptions.RequestException("temporary failure")
    post_mock: MagicMock = MagicMock(side_effect=[first_exc, response])
    time_mock: MagicMock = MagicMock()
    validate_mock: MagicMock = MagicMock()
    sign_mock: MagicMock = MagicMock(return_value="signature-123")
    info_mock: MagicMock = MagicMock()
    error_mock: MagicMock = MagicMock()

    time_mock.time.side_effect = [10.0, 11.0, 20.0, 20.4]
    time_mock.sleep = MagicMock()

    monkeypatch.setattr(client.requests, "post", post_mock)
    monkeypatch.setattr(client, "time", time_mock)
    monkeypatch.setattr(client, "validate", validate_mock)
    monkeypatch.setattr(client, "sign", sign_mock)
    monkeypatch.setattr(client.logger, "info", info_mock)
    monkeypatch.setattr(client.logger, "error", error_mock)

    result = client.submit(sample_payload, dev_endpoint, dev_secret, retries=2)

    assert result == {"ok": True}
    assert post_mock.call_count == 2
    time_mock.sleep.assert_called_once_with(1)
    error_mock.assert_called_once()


def test_submit_raises_after_max_retries(
    monkeypatch: pytest.MonkeyPatch, dev_secret, dev_endpoint, sample_payload
) -> None:
    """Verify that the client raises after exhausting retries."""
    exc = requests.exceptions.RequestException("network down")
    post_mock: MagicMock = MagicMock(side_effect=exc)
    time_mock: MagicMock = MagicMock()
    validate_mock: MagicMock = MagicMock()
    sign_mock: MagicMock = MagicMock(return_value="signature-123")
    info_mock: MagicMock = MagicMock()
    error_mock: MagicMock = MagicMock()

    time_mock.time.side_effect = [1.0, 2.0, 3.0]
    time_mock.sleep = MagicMock()

    monkeypatch.setattr(client.requests, "post", post_mock)
    monkeypatch.setattr(client, "time", time_mock)
    monkeypatch.setattr(client, "validate", validate_mock)
    monkeypatch.setattr(client, "sign", sign_mock)
    monkeypatch.setattr(client.logger, "info", info_mock)
    monkeypatch.setattr(client.logger, "error", error_mock)

    with pytest.raises(Exception, match="Max retries reached"):
        client.submit(sample_payload, dev_endpoint, dev_secret, retries=2)

    assert post_mock.call_count == 2
    assert time_mock.sleep.call_count == 1
    assert error_mock.call_count == 2
