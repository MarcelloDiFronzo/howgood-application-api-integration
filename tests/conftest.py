"""Shared pytest fixtures for environment-dependent tests."""

import os
import time

import pytest
import requests


def _candidate_urls() -> list[str]:
    """Return the possible mock server health-check URLs."""
    return [
        "http://mock-api:8080/health",
        "http://localhost:8080/health",
        "http://127.0.0.1:8080/health",
    ]


@pytest.fixture(scope="session")
def wait_for_mock_server() -> None:
    """Fail the test session if the mock server does not become available."""
    last_error: Exception | None = None

    for url in _candidate_urls():
        for _ in range(3):
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    return
            except Exception as exc:
                last_error = exc
                time.sleep(0.2)

    pytest.fail(
        f"Mock server not available. Tried: {', '.join(_candidate_urls())}. "
        f"Last error: {last_error}"
    )


@pytest.fixture
def dev_secret():
    """Return the dev secret or skip the test when it is unavailable."""
    secret = os.getenv("DEV_HOWGOOD_SECRET")
    if not secret:
        pytest.skip("DEV_HOWGOOD_SECRET is not set")
    return secret


@pytest.fixture
def dev_endpoint():
    """Return the dev endpoint or skip the test when it is unavailable."""
    endpoint = os.getenv("DEV_HOWGOOD_ENDPOINT")

    if not endpoint:
        pytest.skip("DEV_HOWGOOD_ENDPOINT are not set")

    return endpoint
