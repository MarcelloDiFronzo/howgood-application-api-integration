"""HTTP client responsible for validating, signing, and submitting payloads."""

import json
import time

import requests

from howgood_apply.logger import get_logger

from .signer import sign
from .validator import validate

logger = get_logger()


def submit(payload: dict, endpoint: str, secret: str, retries: int = 3):
    """
    Validate the payload, sign it, and submit it with retry handling.

    Retries use exponential backoff for transient network failures.
    """
    validate(payload)

    body = json.dumps(payload, separators=(",", ":"), default=str)
    signature = sign(payload, secret)

    headers = {
        "Content-Type": "application/json",
        "X-HMAC-Signature": signature,
    }

    for attempt in range(retries):
        start = time.time()

        try:
            logger.info("Sending request", attempt=attempt + 1)

            response = requests.post(endpoint, data=body, headers=headers, timeout=10)

            response.raise_for_status()

            latency = time.time() - start

            logger.info(f"Request successful ({response.status_code})", latency=latency)
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error("Request failed", error=str(e))

            if attempt == retries - 1:
                raise Exception("Max retries reached")
            sleep_time = 2**attempt
            logger.info("Retrying...", sleep=sleep_time)
            time.sleep(sleep_time)

    raise Exception("Max retries reached")
