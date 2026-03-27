import pytest

from howgood_apply.client import submit
from howgood_apply.config_loader import load_payload


@pytest.mark.integration
def test_submit_to_mock_server(wait_for_mock_server, dev_secret, dev_endpoint) -> None:
    payload = load_payload()

    response = submit(payload, dev_endpoint, dev_secret)

    assert response["status"] == "received"
    assert "timestamp" in response
    assert isinstance(response["timestamp"], str)
