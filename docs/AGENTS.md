# AI Agents Guide

This document describes how AI agents are used in this project: their roles, prompting patterns, and how to extend and operate them locally.

## Overview
- Goal: build an end-to-end RAG/transcription workflow with modular agents for data ingestion, transcription, chunking, embedding, retrieval, and UI.
- Agent types: developer/coding agent (automation), data/transcription agent, retrieval/answering agent, and evaluation/QA agent.
- Execution surfaces: CLI tasks in `src/`, notebooks in `notebooks/`, and tests in `tests/`.

## Agents and Responsibilities
- Developer Agent: automates repo changes, planning (see `docs/TODO.md`), and logs prompts (see `docs/PROMPTS-LOG.md`).
- Transcription Agent: converts audio to text (see `src/transcriber/`).
- Ingestion Agent: normalizes text, chunks documents, and writes vectorstore (see `src/ingest.py`).
- Retrieval Agent: embeds queries, retrieves top-K results from Chroma (see `src/utils/vectorstore.py`).
- UI Agent: thin presentation layer (e.g., `src/ui.py` or Streamlit/Gradio prototypes).

## Prompting Guidelines
- Be explicit about objectives and constraints. Include target files/paths and acceptance criteria.
- Prefer small, verifiable steps and maintain a visible plan (see `docs/TODO.md`).
- Log meaningful interactions: timestamp, prompt, plan/todo, brief process summary, result (see `docs/PROMPTS-LOG.md`).

## Operating Locally
1. Create and activate a Python environment with `uv` (see pyproject.toml):
   - `uv venv && source .venv/bin/activate`
   - `uv pip install -e .[dev]`
2. Lint and format: `ruff check .`
3. Run tests with coverage: `pytest -q --cov=src --cov-report=term-missing`.
4. Ingest pipeline:
   - Transcribe audio: `python -m src.asr_batch --input_dir data/audio --output data/transcripts_raw`
   - Normalize and chunk: `python -m src.normalize` (if present) and `python -m src.ingest`
5. Notebooks: open `notebooks/pipeline_demo.ipynb` for an end-to-end demo.

## Transcriber API (FastAPI)
- Start server: `python -m src.transcriber.api.run` (defaults to `0.0.0.0:8000`).
- Health: `GET /health` → `{ "status": "ok" }`.
- Upload transcription: `POST /transcribe` (multipart form)
  - Fields: `file` (audio), optional: `language`, `segment_sec`, `use_vad`, `beam`, `timestamps`, `out_dir`.
- Local path transcription: `POST /transcribe/path`
  - Query/body: `file_path` (absolute/relative path), optional: same params as above.
- Both endpoints return `{ payload, jsonl_path }`, where `jsonl_path` is set if `out_dir` is provided.

## Audio Saver API (FastAPI)
- Start server: `python -m src.audio.api.run` (defaults to `0.0.0.0:8001`).
- Health: `GET /health` → `{ "status": "ok" }`.
- Save MP3 by URL: `POST /audio/save` with JSON body
  - `{ "url": "https://…", "out_dir": "data/audio", "filename": "optional_name" }`
  - Uses `yt-dlp` + FFmpeg to extract audio to MP3.
  - Returns `{ "path": "data/audio/<name>.mp3" }`.

## Claude Notes
- This guide also serves as `CLAUDE.md` for teams using Claude-like agents.
- Provide structured tasks with clear input/output artifacts (files, tests) and limit scope per step.
- Capture run logs and decisions into `docs/PROMPTS-LOG.md`.

## Extending Agents
- Add new agents as submodules under `src/<agent_name>` with a clear API and tests under `tests/`.
- Keep responsibilities single-purpose and write thin adapters between modules.

## Prompt Logs and TODOs
- Logs: `docs/PROMPTS-LOG.md` (append entries per prompt/session).
- Roadmap and status: `docs/TODO.md` (Backlog/Next/In progress/To review/Done).
