"""Load environment-based runtime settings."""

import os

from dotenv import load_dotenv

# Load values from .env before reading runtime configuration.
load_dotenv()

env = os.getenv("ENV")

if env == "dev":
    SECRET = os.getenv("DEV_HOWGOOD_SECRET") or ""
    ENDPOINT = os.getenv("DEV_HOWGOOD_ENDPOINT") or ""
elif env == "prod":
    SECRET = os.getenv("PROD_HOWGOOD_SECRET") or ""
    ENDPOINT = os.getenv("PROD_HOWGOOD_ENDPOINT") or ""
else:
    raise ValueError("Invalid ENV")

if not SECRET:
    raise ValueError("Missing HOWGOOD_SECRET")

if not ENDPOINT:
    raise ValueError("Missing HOWGOOD_ENDPOINT")
