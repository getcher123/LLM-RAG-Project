#!/usr/bin/env python3
"""
Real audio transcription using faster-whisper
"""
import json
import time
from pathlib import Path
from typing import Dict, List

from faster_whisper import WhisperModel


def transcribe_with_faster_whisper(
    audio_path: Path, 
    model_size: str = "small", 
    language: str = "ru",
    compute_type: str = "int8"
) -> Dict:
    """
    Transcribe audio file using faster-whisper
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large-v2, large-v3)
        language: Language code
        compute_type: Compute type for inference
    
    Returns:
        Dictionary with transcription results
    """
    print(f"Initializing Whisper model: {model_size}")
    model = WhisperModel(model_size, device="cpu", compute_type=compute_type)
    
    print(f"Transcribing: {audio_path.name}")
    start_time = time.time()
    
    # Transcribe with word-level timestamps
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )
    
    # Process segments
    transcription_segments = []
    full_text_parts = []
    
    for segment in segments:
        segment_dict = {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2), 
            "text": segment.text.strip(),
            "words": []
        }
        
        # Add word-level timestamps if available
        if hasattr(segment, 'words') and segment.words:
            for word in segment.words:
                word_dict = {
                    "start": round(word.start, 2),
                    "end": round(word.end, 2),
                    "word": word.word,
                    "probability": round(word.probability, 3)
                }
                segment_dict["words"].append(word_dict)
        
        transcription_segments.append(segment_dict)
        full_text_parts.append(segment.text.strip())
    
    processing_time = time.time() - start_time
    
    # Create result structure
    result = {
        "file_id": audio_path.stem,
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "duration": round(info.duration, 2),
        "model_size": model_size,
        "processing_time": round(processing_time, 2),
        "segments": transcription_segments,
        "full_text": " ".join(full_text_parts)
    }
    
    print(f"Transcription completed in {processing_time:.2f}s")
    print(f"Audio duration: {info.duration:.2f}s")
    print(f"Language detected: {info.language} (confidence: {info.language_probability:.3f})")
    print(f"Number of segments: {len(transcription_segments)}")
    
    return result


def main():
    # Input and output paths
    audio_file = Path("tmp/audio/В месяц ты зарабатываешь больше 1млн рублей？ Звезда ＂Реутов ТВ＂ у Дудя.mp3")
    output_dir = Path("tmp/real_transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not audio_file.exists():
        print(f"Error: Audio file not found: {audio_file}")
        return
    
    print(f"Starting real transcription for: {audio_file.name}")
    
    # Transcribe
    try:
        result = transcribe_with_faster_whisper(
            audio_file, 
            model_size="small",  # Good balance of speed and accuracy
            language="ru"
        )
        
        # Save result
        output_file = output_dir / f"{result['file_id']}.jsonl"
        with output_file.open("w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, indent=2))
        
        print(f"Real transcript saved: {output_file}")
        
        # Print sample of transcript
        print(f"\nTranscript preview:")
        print(f"Full text length: {len(result['full_text'])} characters")
        print(f"First 200 characters: {result['full_text'][:200]}...")
        
        return result
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


if __name__ == "__main__":
    main()