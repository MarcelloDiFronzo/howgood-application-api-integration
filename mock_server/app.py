"""Mock API server used for integration tests."""

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request

SECRET = os.getenv("DEV_HOWGOOD_SECRET")
if not SECRET:
    raise RuntimeError("Missing required environment variable: SECRET")

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Return a basic health response."""
    return jsonify({"status": "ok"}), 200


def verify_signature(raw_body: bytes, signature: str) -> bool:
    """Verify the request signature against the configured secret."""
    assert SECRET is not None
    expected = hmac.new(SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.route("/apply", methods=["POST"])
def apply():
    """Validate the signature and return a mock success response."""
    raw_body = request.data
    signature = request.headers.get("X-HMAC-Signature")

    if not signature:
        return jsonify({"error": "Missing signature"}), 400

    if not verify_signature(raw_body, signature):
        return jsonify({"error": "Invalid signature"}), 403

    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, ValueError, TypeError):
        return jsonify({"error": "Invalid JSON"}), 400

    return jsonify(
        {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "received",
            "name": payload.get("name"),
        }
    ), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
