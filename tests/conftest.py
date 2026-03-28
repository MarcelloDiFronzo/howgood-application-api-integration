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
    secret = os.getenv("DEV_HOWGOOD_SECRET") or "dev-secret"

    return secret


@pytest.fixture
def dev_endpoint():
    """Return the dev endpoint or skip the test when it is unavailable."""
    endpoint = os.getenv("DEV_HOWGOOD_ENDPOINT") or "http://localhost:8000/apply"

    return endpoint


@pytest.fixture
def sample_payload() -> dict[str, object]:
    """Return a valid sample application payload."""
    return {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "resume": "https://example.com/resume.pdf",
        "location": "Remote",
        "linkedin": "https://linkedin.com/in/janedoe",
        "codeLink": "https://github.com/janedoe",
        "yearsPython": 7,
        "yearsDjango": 3,
        "repos": "https://github.com/janedoe?tab=repositories",
        "notes": "Great candidate",
    }
