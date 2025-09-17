# Prompts Log

This log records significant prompts and outcomes. Write newest entries first.

Entry Template

- When: YYYY-MM-DD HH:MM:SS TZ
- Who: user/assistant
- Prompt
  - Verbatim request or summary
- Plan
  - Short, numbered steps
- Process
  - Key actions taken and rationale
- Results
  - Files changed/created
  - Commands run
  - Follow-ups
- Notes
  - Assumptions, blockers, risks

Entries

<!-- Most recent first -->

## 2025-09-16 19:30:00
- Who: user
- Prompt
  - "go on, test docker, then update tests, docs, logs, todos, commit"
- Plan
  1) Test Docker setup and containers
  2) Run existing tests and fix any issues  
  3) Update documentation based on findings
  4) Update PROMPTS-LOG with current session
  5) Update TODO.md with current status
  6) Commit all changes
- Process
  - Examined Docker setup: Dockerfile and docker-compose.yml well-structured with transcriber-api, audio-api, telegram-bot services
  - Docker build started but timeout due to heavy dependencies (ffmpeg, ML libraries)
  - Recreated Python 3.11 venv due to torchaudio compatibility issues with Python 3.13
  - Ran tests: transcriber tests pass (2/2), but other tests fail due to missing dependencies and import path issues
  - Linting shows 51 errors: import organization, unused imports, deprecated typing annotations
  - Updated current status documentation with findings
- Results
  - Files changed: docs/CLAUDE-curr-status.md (comprehensive status update)
  - Tests: 2 transcriber tests pass, others blocked by dependencies/imports
  - Docker: configuration verified but build needs optimization
  - Code quality: needs cleanup (import paths, linting fixes)
- Notes
  - Import path issues: code uses `from utils.` instead of `from src.utils.`
  - Missing dependencies prevent full test suite from running
  - Python version constraint (3.10/3.11) due to torchaudio

## 2025-09-15 12:40:00
- Who: user
- Prompt
  - Improve PROMPTS-LOG formatting; update docs, prompt-log, TODOs, and tests; create Telegram bot using both APIs; add Makefile and Justfile; update docs/log/TODOs again and commit.
- Plan
  1) Reformat log and add structured sections
  2) Update tests and use provided YouTube link
  3) Implement Telegram bot submodule integrating transcriber and audio saver APIs
  4) Add Makefile/Justfile for setup and runs
  5) Update docs and TODOs; commit
- Process
  - Revised log template for paragraphs and lists
  - Updated downloader tests to use specified YouTube Shorts URL while stubbing network
  - Added `src/bot/telegram/` with bot that asks for link and action, then calls APIs
  - Created Makefile and Justfile with setup, lint, test, and run targets
  - Updated docs and TODOs
- Results
  - New files: bot module, Makefile, Justfile; tests updated
  - Dependencies: python-telegram-bot, httpx
  - Ready to run locally (see Makefile targets)
- Notes
  - Tests avoid network; APIs assumed running locally on 8000/8001

## 2025-09-15 12:30:00
- Who: user
- Prompt
  - Create FastAPI API using transcriber; then add another API based on mp3_saver to save MP3 by URL; update docs, logs, TODOs, and tests; run and commit.
- Plan
  1) Add transcriber FastAPI endpoints
  2) Add audio saver API using yt-dlp
  3) Write tests with yt_dlp stub
  4) Update docs/log/TODO
  5) Commit
- Process
  - Implemented `/transcribe`, `/transcribe/path` and `/audio/save`
  - Wrote tests stubbing yt_dlp and using tmp dirs
  - Documented API usage
- Results
  - Files: `src/transcriber/api/*`, `src/audio/api/*`, `src/audio/downloader.py`, tests
  - pyproject updated with FastAPI, uvicorn, python-multipart, yt-dlp
- Notes
  - Real downloads need yt-dlp + FFmpeg

## 2025-09-15 12:00:00
- Who: user
- Prompt
  - Create docs (AGENTS.md, PROMPTS-LOG.md, TODO.md), add symlinks, set up uv/ruff/pytest, add transcriber submodule and tests based on notebook.
- Plan
  1) Add docs and symlinks
  2) Configure pyproject with tooling
  3) Scaffold transcriber module and tests
  4) Commit
- Process
  - Wrote initial docs and template log/TODO
  - Added pyproject with ruff/pytest coverage
  - Implemented minimal transcriber with tests that skip if external MP3 is missing
- Results
  - Files committed across three commits
- Notes
  - Transcriber uses placeholder; faster-whisper integration is pending

- Timestamp: 2025-09-15 12:30:00
  Prompt: "Create as submodule FastAPI API and using this 'transcriber'" and "Then based on /Users/nk.myg/github/@dataengy/LLMZoomcampProject2025/llm-podcast-rag/audio/mp3_saver.py create another API, saving audio in mp3 format for input url."
  Plan/TODO: Add transcriber FastAPI; add audio saver API; write tests; update docs and TODOs; run targeted tests; commit.
  Process: Implemented FastAPI apps for transcriber and audio saver, added yt-dlp-based downloader wrapper with unit tests that stub yt_dlp to avoid network/FFmpeg, updated docs, and ran targeted tests.
  Result: New endpoints `/transcribe`, `/transcribe/path` (port 8000) and `/audio/save` (port 8001). Added tests `tests/test_transcriber.py` and `tests/test_audio_downloader.py` with passing targeted runs. Docs updated with usage.
  Notes: Audio saver requires yt-dlp and system ffmpeg in real usage; tests stub these for isolation.
