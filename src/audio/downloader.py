from __future__ import annotations

from pathlib import Path
from typing import Optional


def save_mp3_from_url(url: str, out_dir: str | Path = "data/audio", filename: Optional[str] = None) -> Path:
    """
    Download audio from a URL and save as MP3 using yt-dlp + FFmpeg.
    - url: media URL (e.g., YouTube).
    - out_dir: destination directory (created if missing).
    - filename: optional base filename without extension. If omitted, yt-dlp will
      derive from the media title.

    Returns the resulting .mp3 Path.

    Note: Requires `yt-dlp` and system `ffmpeg` installed and available on PATH.
    """
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    try:
        import yt_dlp  # type: ignore
    except Exception as e:  # pragma: no cover
        raise ImportError("yt-dlp is required: pip install yt-dlp") from e

    # Build output template
    if filename:
        outtmpl = str(out_dir_p / f"{filename}.%(ext)s")
    else:
        outtmpl = str(out_dir_p / "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
    }

    # Run yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore[attr-defined]
        ydl.download([url])

    # Determine produced file path. If filename is specified, it's deterministic.
    if filename:
        return out_dir_p / f"{filename}.mp3"

    # Otherwise, search for the most recent mp3 file in out_dir.
    mp3s = sorted(out_dir_p.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp3s:  # pragma: no cover - relies on external ydl
        raise FileNotFoundError("yt-dlp reported success but no MP3 found")
    return mp3s[0]

