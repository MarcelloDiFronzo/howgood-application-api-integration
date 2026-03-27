"""Shared pytest fixtures for environment-dependent tests."""

import os

import pytest


@pytest.fixture
def dev_secret():
    """Return the dev secret or skip the test when it is unavailable."""
    secret = os.getenv("DEV_HOWGOOD_SECRET") or "secret"
    if not secret:
        pytest.skip("DEV_HOWGOOD_SECRET is not set")
    return secret


@pytest.fixture
def dev_endpoint():
    """Return the dev endpoint or skip the test when it is unavailable."""
    endpoint = os.getenv("DEV_HOWGOOD_ENDPOINT") or "localhost:8080"

    if not endpoint:
        pytest.skip("DEV_HOWGOOD_ENDPOINT are not set")

    return endpoint
