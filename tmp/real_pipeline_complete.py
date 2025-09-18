#!/usr/bin/env python3
"""
Complete real pipeline: process real transcript -> normalize -> chunk
"""
import json
from pathlib import Path
from typing import List

def normalize_text_simple(text: str) -> str:
    """Simple text normalization"""
    text = text.strip()
    text = " ".join(text.split())  # normalize whitespace
    # Remove dialog markers for cleaner text
    text = text.replace("—", "").replace("  ", " ").strip()
    return text

def split_into_chunks_by_words(text: str, size: int = 250) -> List[str]:
    """Split text into chunks by word count"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
    
    return chunks

def main():
    # Input and output paths
    real_transcript_file = Path("tmp/real_transcripts/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.jsonl")
    output_dir = Path("tmp")
    
    normalized_dir = output_dir / "real_transcripts_normalized"
    chunks_dir = output_dir / "real_chunks"
    
    # Create directories
    for d in [normalized_dir, chunks_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    print("Processing real transcript through complete pipeline...")
    
    # Load real transcript
    with real_transcript_file.open("r", encoding="utf-8") as f:
        transcript = json.load(f)
    
    print(f"Loaded real transcript: {len(transcript['segments'])} segments, {transcript['duration']}s audio")
    
    # Step 1: Normalize
    print("Step 1: Normalizing text...")
    normalized_text = normalize_text_simple(transcript["full_text"])
    transcript["normalized_text"] = normalized_text
    
    # Save normalized transcript
    normalized_file = normalized_dir / f"{transcript['file_id']}.jsonl"
    with normalized_file.open("w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)
    
    print(f"Normalized transcript saved: {normalized_file}")
    
    # Step 2: Create chunks
    print("Step 2: Creating chunks...")
    chunks = split_into_chunks_by_words(normalized_text, size=100)  # Smaller chunks for better RAG
    
    all_chunks = []
    for i, chunk_text in enumerate(chunks):
        chunk = {
            "id": f"{transcript['file_id']}::{i}",
            "text": chunk_text,
            "metadata": {
                "source_id": transcript['file_id'], 
                "type": "audio",
                "duration": transcript['duration'],
                "language": transcript['language'],
                "model_size": transcript['model_size'],
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
        }
        all_chunks.append(chunk)
    
    # Save chunks
    chunks_file = chunks_dir / "real_chunks.jsonl"
    with chunks_file.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    
    print(f"Real chunks saved: {chunks_file}")
    print(f"Created {len(all_chunks)} chunks")
    
    # Step 3: Create final report
    print("Step 3: Creating final report...")
    real_report = {
        "pipeline_type": "real_transcription", 
        "audio_file": "tmp/audio/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.mp3",
        "real_transcript_file": str(real_transcript_file),
        "normalized_file": str(normalized_file),
        "chunks_file": str(chunks_file),
        "transcription_stats": {
            "duration_seconds": transcript["duration"],
            "language": transcript["language"],
            "language_confidence": transcript["language_probability"], 
            "model_size": transcript["model_size"],
            "processing_time": transcript["processing_time"],
            "num_segments": len(transcript["segments"]),
            "num_chunks": len(all_chunks),
            "full_text_length": len(transcript["full_text"]),
            "normalized_text_length": len(normalized_text)
        },
        "content_preview": {
            "first_100_chars": normalized_text[:100],
            "sample_segment": transcript["segments"][0] if transcript["segments"] else None,
            "sample_chunk": all_chunks[0] if all_chunks else None
        }
    }
    
    report_file = output_dir / "real_pipeline_report.json"
    with report_file.open("w", encoding="utf-8") as f:
        json.dump(real_report, f, ensure_ascii=False, indent=2)
    
    print(f"Real pipeline report saved: {report_file}")
    print("Real transcription pipeline completed successfully!")
    
    print("\n=== SUMMARY ===")
    print(f"✅ Audio transcribed: {transcript['duration']:.1f}s in {transcript['processing_time']:.1f}s")
    print(f"✅ Language detected: {transcript['language']} ({transcript['language_probability']:.3f} confidence)")
    print(f"✅ Segments created: {len(transcript['segments'])}")
    print(f"✅ RAG chunks created: {len(all_chunks)} (100 words each)")
    print(f"✅ Text length: {len(normalized_text)} characters")
    print(f"✅ Content preview: {normalized_text[:100]}...")
    
    return real_report

if __name__ == "__main__":
    main()