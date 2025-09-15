from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl

from src.audio.downloader import save_mp3_from_url


app = FastAPI(title="Audio Saver API", version="0.1.0")


class SaveRequest(BaseModel):
    url: HttpUrl = Field(..., description="Media URL to download")
    out_dir: Optional[str] = Field("data/audio", description="Destination directory")
    filename: Optional[str] = Field(None, description="Base filename without extension")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/audio/save")
def audio_save(req: SaveRequest):
    try:
        path = save_mp3_from_url(str(req.url), req.out_dir or "data/audio", req.filename)
        return {"path": str(path)}
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(e))

