"""Command-line entry point for submitting the application payload."""

from howgood_apply.client import submit
from howgood_apply.config_loader import load_payload
from howgood_apply.logger import get_logger
from howgood_apply.settings import ENDPOINT, SECRET

logger = get_logger()


def main() -> None:
    """Load the payload and submit it using the configured credentials."""
    try:
        logger.info("Loading payload")
        payload = load_payload()

        logger.info("Starting submission from apply.py")
        response = submit(payload, ENDPOINT, SECRET)
        logger.info("Submission complete", response=response)

    except Exception as e:
        logger.error("Submission failed", error=str(e))


if __name__ == "__main__":
    main()
