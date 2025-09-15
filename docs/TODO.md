# Project TODO

Curr status

- Scope: End-to-end RAG pipeline with audio transcription, chunking, embeddings, retrieval, and simple UI. Tooling via `uv`, `ruff`, `pytest`.
- Risks: External model dependencies, local audio availability, vectorstore persistence.
- Next milestone: Transcriber submodule and tests, tooling integration.

Backlog

- Add real faster-whisper integration in `src/utils/audio_utils.py`.
- Expand normalization heuristics beyond simple placeholder.
- Improve retrieval evaluation with gold Q&A.
- Package CLI entry points for pipelines.

Next

- Scaffold `src/transcriber` based on `notebooks/pipeline_demo.ipynb`.
- Add tests for `transcriber` with optional external mp3 path.

In progress

- Documentation and developer workflow setup (this change).

To review

- Docs: `docs/AGENTS.md`, `docs/PROMPTS-LOG.md`, `docs/TODO.md`.

Done

- Repo structure: `src/`, `tests/`, `notebooks/`, `data/`, `configs/`.

