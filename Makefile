.PHONY: help venv install lint test api-transcriber api-audio bot docker-build docker-up docker-down docker-logs

help:
	@echo "Targets: venv, install, lint, test, api-transcriber, api-audio, bot"
	@echo "Docker: docker-build, docker-up, docker-down, docker-logs"

venv:
	uv venv && . .venv/bin/activate

install:
	uv pip install -e .[dev]

lint:
	ruff check .

test:
	pytest -q --cov=src --cov-report=term-missing

api-transcriber:
	python -m src.transcriber.api.run

api-audio:
	python -m src.audio.api.run

bot:
	TELEGRAM_BOT_TOKEN=$$TELEGRAM_BOT_TOKEN python -m src.bot.telegram_bot

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

