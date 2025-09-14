from pathlib import Path
from typing import Dict


def run_batch_asr(input_dir: Path, language: str = "ru", segment_sec: int = 60, use_vad: bool = False, beam: int = 5, timestamps: str = "segment") -> Dict[str, dict]:
    """
    Placeholder batch ASR runner. Replace with faster-whisper integration.
    Returns a dict: file_id -> {file_id, language, segments[], full_text}
    """
    results = {}
    for p in sorted(input_dir.glob("*")):
        if p.suffix.lower() not in {".mp3", ".wav", ".m4a", ".mp4"}:
            continue
        file_id = p.stem
        payload = {
            "file_id": file_id,
            "language": language,
            "segments": [
                {"start": 0.0, "end": 5.0, "speaker": "spk1", "text": "(demo) пример транскрипта"}
            ],
            "full_text": "(demo) пример транскрипта"
        }
        results[file_id] = payload
    return results

