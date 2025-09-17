set shell := ["bash", "-cu"]

default:
  @just --list

# Environment
venv:
  uv venv && source .venv/bin/activate && echo "venv ready"

install:
  source .venv/bin/activate && uv pip install -e .[dev]

# Diagnostics
versions:
  python --version || true
  uv --version || true
  ruff --version || true
  pytest --version || true

lint:
  ruff check .

test:
  pytest -q --cov=src --cov-report=term-missing

# Run services
api-transcriber:
  python -m src.transcriber.api.run

api-audio:
  python -m src.audio.api.run

bot:
  TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN} python -m src.bot.telegram_bot

# Docker commands
docker-build:
  docker-compose build

docker-up:
  docker-compose up -d

docker-down:
  docker-compose down

docker-logs:
  docker-compose logs -f

docker-restart:
  docker-compose restart

