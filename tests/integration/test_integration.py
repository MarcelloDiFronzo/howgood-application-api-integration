import pytest

from howgood_apply.client import submit


@pytest.mark.integration
def test_submit_to_mock_server(
    wait_for_mock_server, dev_secret, dev_endpoint, sample_payload
) -> None:
    response = submit(sample_payload, dev_endpoint, dev_secret)

    assert response["status"] == "received"
    assert "timestamp" in response
    assert isinstance(response["timestamp"], str)
