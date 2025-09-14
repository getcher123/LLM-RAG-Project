import argparse
import json
import os
from pathlib import Path
from dotenv import load_dotenv

from utils.audio_utils import run_batch_asr


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Batch ASR with Whisper v3 Medium")
    parser.add_argument("--input_dir", default="data/audio", help="Directory with audio files")
    parser.add_argument("--output", default="data/transcripts_raw", help="Output dir for JSONL transcripts")
    parser.add_argument("--language", default="ru")
    parser.add_argument("--segment_sec", type=int, default=60)
    parser.add_argument("--vad", action="store_true")
    parser.add_argument("--beam", type=int, default=5)
    parser.add_argument("--timestamps", default="segment", choices=["none", "segment", "word"])
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = run_batch_asr(
        input_dir=input_dir,
        language=args.language,
        segment_sec=args.segment_sec,
        use_vad=args.vad,
        beam=args.beam,
        timestamps=args.timestamps,
    )

    # Write one JSONL per input file
    for file_id, payload in results.items():
        out_path = output_dir / f"{file_id}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    print(f"Saved {len(results)} transcript(s) to {output_dir}")


if __name__ == "__main__":
    main()

