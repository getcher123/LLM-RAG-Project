from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

from src.transcriber.core import transcribe_file, transcribe_to_jsonl


app = FastAPI(title="Transcriber API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe_upload(
    file: UploadFile = File(...),
    language: str = Form("ru"),
    segment_sec: int = Form(60),
    use_vad: bool = Form(False),
    beam: int = Form(5),
    timestamps: Literal["none", "segment", "word"] = Form("segment"),
    out_dir: Optional[str] = Form(None),
):
    """
    Transcribe an uploaded audio file. Optionally write a JSONL to `out_dir`.
    Returns the transcription payload and, if written, the output path.
    """
    # Save the uploaded file to a temp location
    try:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in {".mp3", ".wav", ".m4a", ".mp4"}:
            raise HTTPException(status_code=400, detail=f"Unsupported extension: {suffix}")

        tmp_path = Path("data/audio") / f"upload_{file.filename}"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        content = await file.read()
        tmp_path.write_bytes(content)

        payload = transcribe_file(
            tmp_path,
            language=language,
            segment_sec=segment_sec,
            use_vad=use_vad,
            beam=beam,
            timestamps=timestamps,
        )

        out_path_str = None
        if out_dir:
            out_path = transcribe_to_jsonl(
                tmp_path,
                out_dir,
                language=language,
                segment_sec=segment_sec,
                use_vad=use_vad,
                beam=beam,
                timestamps=timestamps,
            )
            out_path_str = str(out_path)

        return {"payload": payload, "jsonl_path": out_path_str}
    except HTTPException:
        raise
    except Exception as e:  # pragma: no cover - simple error pass-through
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe/path")
def transcribe_from_path(
    file_path: str,
    language: str = "ru",
    segment_sec: int = 60,
    use_vad: bool = False,
    beam: int = 5,
    timestamps: Literal["none", "segment", "word"] = "segment",
    out_dir: Optional[str] = None,
):
    """
    Transcribe an existing file on disk. Optionally write a JSONL to `out_dir`.
    """
    p = Path(file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    try:
        payload = transcribe_file(
            p,
            language=language,
            segment_sec=segment_sec,
            use_vad=use_vad,
            beam=beam,
            timestamps=timestamps,
        )
        out_path_str = None
        if out_dir:
            out_path = transcribe_to_jsonl(
                p,
                out_dir,
                language=language,
                segment_sec=segment_sec,
                use_vad=use_vad,
                beam=beam,
                timestamps=timestamps,
            )
            out_path_str = str(out_path)
        return {"payload": payload, "jsonl_path": out_path_str}
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(e))

