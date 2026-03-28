PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python
RUFF=$(VENV)/bin/ruff
MYPY=$(VENV)/bin/mypy
IMAGE_NAME=my-app

ifneq (,$(wildcard .env))
include .env
export
endif

reset:
	rm -rf $(VENV)
	$(MAKE) install

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

clean:
	$(MAKE) docker-stop
	rm -rf $(VENV)
	rm -rf howgood_apply.egg-info
	rm -rf build

run:
	$(PY) apply.py

lint:
	$(RUFF) check .

typecheck:
	$(MYPY) .

test-unit:
	$(PY) -m pytest -q -m "not integration"

test-integration:
	$(PY) -m pytest -q -m integration

ci:
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test-unit
	$(MAKE) docker-build
	$(MAKE) docker-run
	$(MAKE) test-integration
	$(MAKE) docker-logs
	$(MAKE) docker-stop

format:
	$(RUFF) check . --fix
	$(RUFF) format .

cli:
	$(PY) -m howgood_apply.cli --config config/payload.json

docker-build:
	@if docker buildx version >/dev/null 2>&1; then \
		DOCKER_BUILDKIT=1 docker buildx build --load -t $(IMAGE_NAME) mock_server/; \
	else \
		docker build -t $(IMAGE_NAME) mock_server/; \
	fi

docker-run:
	@docker rm -f howgood-app >/dev/null 2>&1 || true
	@export DEV_HOWGOOD_SECRET=$$(grep '^DEV_HOWGOOD_SECRET=' .env | cut -d= -f2-) && \
	docker run -d --name howgood-app \
		-p 8080:8080 \
		-e DEV_HOWGOOD_SECRET \
		$(IMAGE_NAME)

docker-logs:
	docker logs howgood-app

docker-logs-interactive:
	docker logs -f howgood-app

docker-stop:
	@docker rm -f howgood-app >/dev/null 2>&1 || true
