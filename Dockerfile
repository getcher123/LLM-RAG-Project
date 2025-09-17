FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml requirements.txt ./

# Install Python dependencies
RUN uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install -e .[dev]

# Copy source code
COPY . .

# Create data directories
RUN mkdir -p data/audio data/transcripts_raw data/transcripts_normalized data/chunks data/chroma_db

# Activate virtual environment for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Expose ports
EXPOSE 8000 8001

# Default command
CMD ["python", "-m", "src.transcriber.api.run"]