"""CLI entry point for submitting a payload from a custom JSON file."""

import argparse

from howgood_apply.client import submit
from howgood_apply.config_loader import load_payload
from howgood_apply.logger import get_logger
from howgood_apply.settings import ENDPOINT, SECRET

logger = get_logger()


def main() -> None:
    """Parse CLI arguments, load the payload, and submit it."""
    try:
        parser = argparse.ArgumentParser(description="Submit HowGood application")

        parser.add_argument("--config", default="config/payload.json")

        logger.info("Parsing arguments...")
        args = parser.parse_args()

        logger.info(f"Loading payload from {args.config}")
        payload = load_payload(args.config)

        logger.info("Starting submission from cli.py")
        response = submit(payload, ENDPOINT, SECRET)

        logger.info("Submission complete", response=response)

    except Exception as e:
        logger.error("Submission failed", error=str(e))


if __name__ == "__main__":
    main()
