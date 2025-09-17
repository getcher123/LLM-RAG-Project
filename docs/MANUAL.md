# LLM-RAG-Project Manual

## Project Overview

This is an end-to-end RAG (Retrieval-Augmented Generation) system with audio transcription, chunking, embeddings, and retrieval capabilities. The project includes:

- **Audio processing**: Download audio from URLs (YouTube, etc.) and transcribe to text
- **Transcription**: Convert audio to text using Whisper-based ASR
- **RAG pipeline**: Text chunking, embeddings, vectorstore, and retrieval
- **APIs**: FastAPI services for transcription and audio processing
- **Telegram Bot**: User-friendly interface for audio processing workflows

## Quick Start

### Environment Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Unix/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e .[dev]
```

### Using Makefile/Justfile

```bash
# Setup
make venv install

# Development
make lint test

# Services
make api-transcriber  # Port 8000
make api-audio        # Port 8001
make bot             # Requires TELEGRAM_BOT_TOKEN

# Alternative with justfile
just install
just test
just api-transcriber
```

## Core Components

### 1. Audio Processing (`src/audio/`)

**Audio Saver API** (Port 8001):
- Downloads audio from URLs using `yt-dlp`
- Converts to MP3 format
- Endpoint: `POST /audio/save`

```bash
# Start audio API
python -m src.audio.api.run

# Example usage
curl -X POST "http://127.0.0.1:8001/audio/save" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=...", "out_dir": "data/audio"}'
```

### 2. Transcription (`src/transcriber/`)

**Transcriber API** (Port 8000):
- Transcribes audio files to text
- Supports upload and local path processing
- Endpoints: `POST /transcribe`, `POST /transcribe/path`

```bash
# Start transcriber API
python -m src.transcriber.api.run

# Upload file
curl -X POST "http://127.0.0.1:8000/transcribe" \
  -F "file=@audio.mp3"

# Process local file
curl -X POST "http://127.0.0.1:8000/transcribe/path" \
  -d "file_path=/path/to/audio.mp3"
```

### 3. RAG Pipeline (`src/`)

- **`ingest.py`**: Text chunking and vectorstore creation
- **`normalize.py`**: Text normalization and cleanup
- **`serve.py`**: RAG query processing
- **`ui.py`**: Gradio interface

### 4. Telegram Bot (`src/bot/telegram_bot.py`)

Interactive bot for processing YouTube links with options:
- Send MP3 file
- Transcribe only
- Both MP3 and transcription

## Project Structure

```
LLM-RAG-Project/
├── src/
│   ├── audio/           # Audio processing and API
│   ├── bot/             # Telegram bot
│   ├── transcriber/     # Transcription API and logic
│   ├── utils/           # Utilities (vectorstore, embeddings, etc.)
│   ├── asr_batch.py     # Batch audio processing
│   ├── ingest.py        # Text chunking and indexing
│   ├── normalize.py     # Text normalization
│   ├── serve.py         # RAG serving
│   └── ui.py           # Gradio UI
├── tests/              # Test suite
├── docs/               # Documentation
├── data/               # Data directory
├── notebooks/          # Jupyter notebooks
├── Makefile           # Make targets
├── justfile           # Just targets
└── pyproject.toml     # Project configuration
```

## Configuration

### Environment Variables

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# API Endpoints (defaults)
AUDIO_API_BASE=http://127.0.0.1:8001
TRANSCRIBER_API_BASE=http://127.0.0.1:8000
```

### Python Environment

- **Python**: >=3.10
- **Package Manager**: `uv` (recommended)
- **Dependencies**: See `pyproject.toml`

## Development Workflow

### Testing

```bash
# Run tests with coverage
pytest -q --cov=src --cov-report=term-missing

# Or using make/just
make test
just test
```

### Linting

```bash
# Check code style
ruff check .

# Or using make/just
make lint
just lint
```

### Running Services

1. **Start APIs in separate terminals:**
   ```bash
   # Terminal 1: Transcriber API
   make api-transcriber

   # Terminal 2: Audio API
   make api-audio
   ```

2. **Run Telegram Bot:**
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token"
   make bot
   ```

## Usage Examples

### 1. Process YouTube Video via Bot

1. Start both APIs (`make api-transcriber`, `make api-audio`)
2. Start bot with token (`TELEGRAM_BOT_TOKEN=... make bot`)
3. Send YouTube URL to bot
4. Choose processing option (MP3, transcription, or both)

### 2. Direct API Usage

```python
import httpx

# Download audio
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://127.0.0.1:8001/audio/save",
        json={"url": "https://youtube.com/...", "out_dir": "data/audio"}
    )
    audio_path = response.json()["path"]

# Transcribe
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://127.0.0.1:8000/transcribe/path",
        params={"file_path": audio_path}
    )
    transcript = response.json()["payload"]["full_text"]
```

### 3. CLI Processing

```bash
# Batch ASR
python -m src.asr_batch --input_dir data/audio --output data/transcripts_raw

# Normalize transcripts
python -m src.normalize

# Build vector index
python -m src.ingest

# Serve RAG
python -m src.serve
```

## Tech Stack

- **Audio**: `yt-dlp`, `librosa`, `torchaudio`
- **ASR**: `faster-whisper` (Whisper v3)
- **Embeddings**: `sentence-transformers` (multilingual-e5-large-instruct)
- **Vector Store**: `chromadb`
- **Web Framework**: `fastapi`, `uvicorn`
- **UI**: `gradio`, `streamlit`
- **Bot**: `python-telegram-bot`
- **Dev Tools**: `pytest`, `ruff`, `uv`

## Health Checks

### API Health

```bash
# Transcriber API
curl http://127.0.0.1:8000/health

# Audio API
curl http://127.0.0.1:8001/health
```

Both should return `{"status": "ok"}`.

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000/8001 are free
2. **Missing dependencies**: Run `uv pip install -e .[dev]`
3. **Bot token**: Export `TELEGRAM_BOT_TOKEN` environment variable
4. **Audio download**: Requires `yt-dlp` and `ffmpeg`

### Logs and Debugging

- Check API logs in terminal output
- Bot errors appear in console
- Test individual components with pytest

## Current Status

**Latest commits** (dev-hnkovr branch):
- ✅ Telegram bot implementation
- ✅ Audio saver API with yt-dlp integration
- ✅ Transcriber API with upload/path endpoints
- ✅ Test suite with coverage
- ✅ Makefile/Justfile automation

**In Progress**:
- Real faster-whisper integration
- Bot UX improvements
- API auth and rate limiting

**Next Steps**:
- Dockerization
- CLI batch processing integration
- Enhanced RAG pipeline evaluation