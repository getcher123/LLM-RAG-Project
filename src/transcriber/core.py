from __future__ import annotations

from pathlib import Path
from typing import Dict, Literal, Optional


AudioExt = {".mp3", ".wav", ".m4a", ".mp4"}


def _validate_audio_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    if path.suffix.lower() not in AudioExt:
        raise ValueError(f"Unsupported audio extension: {path.suffix}")


def transcribe_file(
    file_path: str | Path,
    *,
    language: str = "ru",
    segment_sec: int = 60,
    use_vad: bool = False,
    beam: int = 5,
    timestamps: Literal["none", "segment", "word"] = "segment",
) -> Dict[str, object]:
    """
    Transcribe a single audio file into a payload dict.

    This is a lightweight wrapper designed to mirror the batch format used in
    the project, returning a dict with keys: file_id, language, segments, full_text.
    The current implementation is a minimal placeholder; integrate faster-whisper
    for production in `utils/audio_utils.py` and reuse here.
    """
    p = Path(file_path)
    _validate_audio_path(p)

    # Minimal placeholder payload for CI/testability without heavy dependencies.
    # Replace with a call to a real transcriber when available.
    file_id = p.stem
    payload = {
        "file_id": file_id,
        "language": language,
        "segments": [
            {
                "start": 0.0,
                "end": 1.0,
                "speaker": "spk1",
                "text": f"(demo) transcript for {p.name}",
            }
        ],
        "full_text": f"(demo) transcript for {p.name}",
        "source_path": str(p),
    }
    return payload


def transcribe_to_jsonl(
    file_path: str | Path,
    out_dir: str | Path,
    *,
    language: str = "ru",
    segment_sec: int = 60,
    use_vad: bool = False,
    beam: int = 5,
    timestamps: Literal["none", "segment", "word"] = "segment",
) -> Path:
    """
    Transcribe a file and write a single-line JSONL file under `out_dir`.
    Returns the output path.
    """
    import json

    result = transcribe_file(
        file_path,
        language=language,
        segment_sec=segment_sec,
        use_vad=use_vad,
        beam=beam,
        timestamps=timestamps,
    )
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)
    out_path = out_dir_p / f"{Path(file_path).stem}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")
    return out_path

