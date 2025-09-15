# Prompts Log

Structured log of user-entered prompts and agent runs. Append new entries at the top.

Template

- Timestamp: YYYY-MM-DD HH:MM:SS TZ
- Prompt: <verbatim user prompt>
- Plan/TODO: <bullet list of steps or reference to docs/TODO.md items>
- Process: <short description of what was done>
- Result: <detailed outcome; files created/updated; commands run; follow-ups>
- Notes: <pitfalls, assumptions, gaps>

Entries

<!-- Most recent first -->

- Timestamp: 2025-09-15 12:30:00
  Prompt: "Create as submodule FastAPI API and using this 'transcriber'" and "Then based on /Users/nk.myg/github/@dataengy/LLMZoomcampProject2025/llm-podcast-rag/audio/mp3_saver.py create another API, saving audio in mp3 format for input url."
  Plan/TODO: Add transcriber FastAPI; add audio saver API; write tests; update docs and TODOs; run targeted tests; commit.
  Process: Implemented FastAPI apps for transcriber and audio saver, added yt-dlp-based downloader wrapper with unit tests that stub yt_dlp to avoid network/FFmpeg, updated docs, and ran targeted tests.
  Result: New endpoints `/transcribe`, `/transcribe/path` (port 8000) and `/audio/save` (port 8001). Added tests `tests/test_transcriber.py` and `tests/test_audio_downloader.py` with passing targeted runs. Docs updated with usage.
  Notes: Audio saver requires yt-dlp and system ffmpeg in real usage; tests stub these for isolation.
