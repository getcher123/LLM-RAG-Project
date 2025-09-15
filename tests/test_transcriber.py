import os
from pathlib import Path

import pytest

from src.transcriber import transcribe_file, transcribe_to_jsonl


EXTERNAL_MP3 = "/Users/nk.myg/github/@dataengy/LLMZoomcampProject2025/llm-podcast-rag/.archive/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.mp3"


def test_transcribe_external_mp3_if_present(tmp_path: Path):
    path = Path(EXTERNAL_MP3)
    if not path.exists():
        pytest.skip("External MP3 not available on this machine")

    result = transcribe_file(path)
    assert isinstance(result, dict)
    assert result.get("file_id") == path.stem
    assert "full_text" in result and isinstance(result["full_text"], str)
    assert result.get("source_path") == str(path)

    out_path = transcribe_to_jsonl(path, tmp_path)
    assert out_path.exists()
    assert out_path.suffix == ".jsonl"


def test_transcribe_unsupported_extension(tmp_path: Path):
    dummy = tmp_path / "dummy.txt"
    dummy.write_text("hello")
    with pytest.raises(ValueError):
        transcribe_file(dummy)

