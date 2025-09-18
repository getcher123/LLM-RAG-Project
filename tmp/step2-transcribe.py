from pathlib import Path

from src.transcriber import transcribe_file, transcribe_to_jsonl

EXTERNAL_MP3 = "/Users/nk.myg/github/@dataengy/LLMZoomcampProject2025/llm-podcast-rag/.archive/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.mp3"
res_path = "/Users/nk.myg/github/@getcher123/LLM-RAG-Project/tmp/"

def transcribe_external_mp3_if_present(path: Path):
    path=Path(path)
    if not path.exists():
        raise FileNotFoundError("External MP3 not available on this machine")

    result = transcribe_file(path)
    assert isinstance(result, dict)
    assert result.get("file_id") == path.stem
    assert "full_text" in result and isinstance(result["full_text"], str)
    assert result.get("source_path") == str(path)

    out_path = transcribe_to_jsonl(path, res_path)
    assert out_path.exists()
    assert out_path.suffix == ".jsonl"


if __name__ == '__main__':
    transcribe_external_mp3_if_present(EXTERNAL_MP3)