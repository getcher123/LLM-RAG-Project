#!/usr/bin/env python3
"""
Complete pipeline runner: transcribe -> normalize -> ingest
"""
import json
import os
from pathlib import Path
from typing import Dict, List

def mock_transcribe_audio(file_path: Path) -> Dict:
    """
    Mock transcription function - in real implementation would use faster-whisper
    """
    file_id = file_path.stem
    
    # For demonstration, we'll create a mock transcript
    mock_segments = [
        {"start": 0.0, "end": 30.0, "speaker": "spk1", "text": "Привет, меня зовут Юрий Дудь"},
        {"start": 30.0, "end": 60.0, "speaker": "spk2", "text": "И сегодня у нас в гостях звезда Реутов ТВ"},
        {"start": 60.0, "end": 90.0, "speaker": "spk1", "text": "Расскажите, в месяц вы зарабатываете больше миллиона рублей?"},
        {"start": 90.0, "end": 120.0, "speaker": "spk2", "text": "Это очень личный вопрос, но я могу сказать что работаю в медиа индустрии"},
        {"start": 120.0, "end": 150.0, "speaker": "spk1", "text": "Понятно, а как вы попали в команду Реутов ТВ?"},
    ]
    
    full_text = " ".join([seg["text"] for seg in mock_segments])
    
    return {
        "file_id": file_id,
        "language": "ru",
        "segments": mock_segments,
        "full_text": full_text
    }

def normalize_text_simple(text: str) -> str:
    """
    Simple text normalization
    """
    # Basic cleanup
    text = text.strip()
    text = " ".join(text.split())  # normalize whitespace
    return text

def split_into_chunks_by_words(text: str, size: int = 250) -> List[str]:
    """
    Split text into chunks by word count
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
    
    return chunks

def main():
    # File paths
    audio_file = Path("tmp/audio/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.mp3")
    output_dir = Path("tmp")
    
    transcripts_dir = output_dir / "transcripts_raw"
    normalized_dir = output_dir / "transcripts_normalized" 
    chunks_dir = output_dir / "chunks"
    
    # Create directories
    for d in [transcripts_dir, normalized_dir, chunks_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting pipeline for: {audio_file.name}")
    
    # Step 1: Transcribe
    print("Step 1: Transcribing audio...")
    transcript = mock_transcribe_audio(audio_file)
    
    # Save raw transcript
    transcript_file = transcripts_dir / f"{transcript['file_id']}.jsonl"
    with transcript_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(transcript, ensure_ascii=False) + "\n")
    
    print(f"Raw transcript saved: {transcript_file}")
    
    # Step 2: Normalize
    print("Step 2: Normalizing text...")
    normalized_text = normalize_text_simple(transcript["full_text"])
    transcript["normalized_text"] = normalized_text
    
    # Save normalized transcript
    normalized_file = normalized_dir / f"{transcript['file_id']}.jsonl" 
    with normalized_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(transcript, ensure_ascii=False) + "\n")
    
    print(f"Normalized transcript saved: {normalized_file}")
    
    # Step 3: Create chunks
    print("Step 3: Creating chunks...")
    chunks = split_into_chunks_by_words(normalized_text, size=250)
    
    all_chunks = []
    for i, chunk_text in enumerate(chunks):
        chunk = {
            "id": f"{transcript['file_id']}::{i}",
            "text": chunk_text,
            "metadata": {"source_id": transcript['file_id'], "type": "audio"}
        }
        all_chunks.append(chunk)
    
    # Save chunks
    chunks_file = chunks_dir / "chunks.jsonl"
    with chunks_file.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    
    print(f"Chunks saved: {chunks_file}")
    print(f"Created {len(all_chunks)} chunks")
    
    # Step 4: Create summary report
    print("Step 4: Creating summary report...")
    report = {
        "pipeline_completed": True,
        "audio_file": str(audio_file),
        "transcript_file": str(transcript_file),
        "normalized_file": str(normalized_file), 
        "chunks_file": str(chunks_file),
        "num_segments": len(transcript["segments"]),
        "num_chunks": len(all_chunks),
        "full_text_length": len(transcript["full_text"]),
        "normalized_text_length": len(normalized_text)
    }
    
    report_file = output_dir / "pipeline_report.json"
    with report_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Pipeline report saved: {report_file}")
    print("Pipeline completed successfully!")
    
    return report

if __name__ == "__main__":
    main()