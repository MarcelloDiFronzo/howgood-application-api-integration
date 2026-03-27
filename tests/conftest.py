"""Shared pytest fixtures for environment-dependent tests."""

import os

import pytest


@pytest.fixture
def dev_secret():
    """Return the dev secret or skip the test when it is unavailable."""
    secret = os.getenv("DEV_HOWGOOD_SECRET")
    if not secret:
        pytest.skip("DEV_HOWGOOD_SECRET is not set")
    return secret
