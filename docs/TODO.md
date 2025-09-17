# Project TODO

Curr status

- Scope: End-to-end RAG pipeline with audio transcription, chunking, embeddings, retrieval, and simple UI. Tooling via `uv`, `ruff`, `pytest`.
- Risks: External model dependencies, local audio availability, vectorstore persistence.
- Next milestone: Wire real faster-whisper + integrate audio saver in pipelines; deploy Telegram bot.

Backlog

- Add real faster-whisper integration in `src/utils/audio_utils.py`.
- Expand normalization heuristics beyond simple placeholder.
- Improve retrieval evaluation with gold Q&A.
- Package CLI entry points for pipelines.

Next

- Integrate `src/audio/downloader.py` with CLI for batch saves by URL list.
- Add API auth/CORS and rate limiting.
- Dockerize APIs and bot.

In progress

- Evaluate switching transcriber placeholder to faster-whisper.
- Bot UX improvements (error messages, progress updates).
- Fix import path issues (change `from utils.` to `from src.utils.`).
- Install missing dependencies for full test coverage.
- Address linting errors (51 total): import organization, deprecated typing.

To review

- Docs: `docs/AGENTS.md`, `docs/PROMPTS-LOG.md`, `docs/TODO.md`.
- Docker setup optimization (build time, dependency management).
- Test infrastructure improvements (dependency management, import fixes).

Done

- Repo structure: `src/`, `tests/`, `notebooks/`, `data/`, `configs/`.
- Transcriber submodule and tests.
- FastAPI transcriber API.
- Audio saver API and downloader utility with tests.
- Telegram bot scaffolding integrated with APIs.
- Makefile and Justfile for setup and runs.
- Docker configuration verification and testing.
- Comprehensive project status documentation update.
- Test coverage analysis (transcriber tests pass, others need dependencies).
