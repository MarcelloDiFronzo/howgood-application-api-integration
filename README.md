# HowGood Application Submission

![CI](https://github.com/MarcelloDiFronzo/howgood-application-api-integration/actions/workflows/ci.yml/badge.svg)

This repository contains a production-style implementation of a signed API integration, built as part of the HowGood application process.

The project is intentionally structured like a small production codebase: configuration is externalized, the client retries failed requests, logging is centralized, and tests are split between unit and integration coverage.

---

## Overview

The application is submitted by sending a signed HTTP POST request to the HowGood API.

- Payload is JSON
- Signature is HMAC-SHA256 of the raw body
- Transport via HTTPS

---

## Features

- Deterministic HMAC-SHA256 signing
- Pydantic-based payload validation
- JSON payload loading from disk
- Environment-based configuration
- CLI entry point
- Retry logic with exponential backoff
- Structured logging with `loguru`
- Unit and integration tests

---

## Project Structure

```Bash
bash
.
├── apply.py
├── config
│ └── payload.json
├── .editorconfig
├── .env
├── .github
│ └── workflows
│     └── ci.yml
├── .gitignore
├── howgood_apply
│ ├── client.py
│ ├── cli.py
│ ├── config_loader.py
│ ├── __init__.py
│ ├── logger.py
│ ├── settings.py
│ ├── signer.py
│ └── validator.py
├── Makefile
├── mock_server
│ ├── app.py
│ ├── Dockerfile
│ └── mock_server_requirements.txt
├── mypy.ini
├── .pre-commit-config.yaml
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── .ruff.toml
├── tests
│ ├── conftest.py
│ ├── __init__.py
│ ├── integration
│ │ └── test_integration.py
│ └── unit
│     ├── test_apply.py
│     ├── test_client.py
│     ├── test_cli.py
│     ├── test_config_loader.py
│     ├── test_logger.py
│     ├── test_settings.py
│     ├── test_signer.py
│     └── test_validator.py
└── utils
    ├── .template_env
    └── template_payload.json
```
## Shortcut commands

    make reset                      # delete the current environment and start over
    make install                    # create and activate the virtual environment, then install dependencies and the package
    make clean                      # stop the mock server and remove the virtual environment, build artifacts
    make run                        # run the main script from the root directory apply.py
    make lint                       # run static checks
    make typecheck                  # run type checks
    make test-unit                  # run unit tests
    make test-integration           # run integration tests
    make ci                         # run all tests and checks
    make format                     # format code
    make cli                        # run the main script using the package's CLI
    make docker-build               # build docker image
    make docker-run                 # run docker container
    make docker-logs                # view docker container logs
    make docker-logs-interactive    # view docker container logs interactively
    make docker-stop                # stop docker container

## Requirements

- Python 3.12+
- `virtualenv` for local environment management

## Installation

Create and activate the virtual environment, then install dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt pip install -e .

or, if you want to use the `Makefile`:

if you don't have a virtualenv:

    make install

or, if you want to delete the current environment and start over:

    make reset

## Configuration
### Payload and environment variables

There are already a `.template_env` and a `template_payload.json` file in the
utils' folder:

- Move the first to the root folder and rename it: `.env`, then, fill in the
proper values.
- Move the `config/payload.json` file from the utils' folder to the `config`
folder and fill in the proper values.

The application reads configuration from `.env` via `python-dotenv`.

### Required variables

Set the environment mode and matching credentials:

    env ENV=dev DEV_HOWGOOD_SECRET=... DEV_HOWGOOD_ENDPOINT=.../apply

For production mode:

    env ENV=prod PROD_HOWGOOD_SECRET=... PROD_HOWGOOD_ENDPOINT=.../apply

## Running the application
### From the root directory
Make sure to have a `.env` file in the root folder and a `payload.json`
file in the `config/` folder.

Set the `ENV` variable to `dev` or `prod` depending on the environment.

Run the main script:

    python apply.py

or use the makefile shortcut:

    make run

or use the CLI (--config is optional):

    python howgood_apply/cli --config config/payload.json

or with the application's entry point (--config is optional):

    howgood-apply --config config/payload.json

## Testing

## Mock server

The repository includes a mock server under `mock_server/`.

To run the mock server:

    make docker-run

To view the logs:

    make docker-logs-interactive
or

    make docker-logs

To stop the mock server:

    make docker-stop

### Unit tests

Run only unit tests:

    python -m pytest -q -m "not integration"

### Integration tests

Run the integration test suite:

    python -m pytest -q -m integration

The integration test requires the mock server to be available.

## Code quality

Run all tests and checks:

    make ci

## Cleaning up
The following command stops the mock server and removes the virtual environment,
build artifacts

    make clean

## Notes

- Payload validation is handled with Pydantic before submission.
- The request body is signed exactly as transmitted to keep the signature
  deterministic.
- The project uses a `pytest.ini` file to register the `integration` marker.

### Final Notes
It has been fun to work on this small project! Thanks.

## Author

Marcello Di Fronzo Gravallese
https://linkedin.com/in/marcello-di-fronzo-gravallese
