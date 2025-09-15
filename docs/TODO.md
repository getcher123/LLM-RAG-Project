# Project TODO

Curr status

- Scope: End-to-end RAG pipeline with audio transcription, chunking, embeddings, retrieval, and simple UI. Tooling via `uv`, `ruff`, `pytest`.
- Risks: External model dependencies, local audio availability, vectorstore persistence.
- Next milestone: Wire real faster-whisper + integrate audio saver in pipelines.

Backlog

- Add real faster-whisper integration in `src/utils/audio_utils.py`.
- Expand normalization heuristics beyond simple placeholder.
- Improve retrieval evaluation with gold Q&A.
- Package CLI entry points for pipelines.

Next

- Integrate `src/audio/downloader.py` with CLI for batch saves by URL list.
- Add API auth/CORS and rate limiting.

In progress

- Evaluate switching transcriber placeholder to faster-whisper.

To review

- Docs: `docs/AGENTS.md`, `docs/PROMPTS-LOG.md`, `docs/TODO.md`.

Done

Done

- Repo structure: `src/`, `tests/`, `notebooks/`, `data/`, `configs/`.
- Transcriber submodule and tests.
- FastAPI transcriber API.
- Audio saver API and downloader utility with tests.
