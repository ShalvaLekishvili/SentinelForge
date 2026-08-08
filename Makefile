.PHONY: install dev test lint run docker

install:
	python -m pip install -r requirements-dev.txt

dev:
	uvicorn backend.main:app --reload

run:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check backend tests

docker:
	docker compose up --build
