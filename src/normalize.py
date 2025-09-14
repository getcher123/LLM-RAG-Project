import argparse
from pathlib import Path
import json
from dotenv import load_dotenv

from utils.text_utils import normalize_text_simple


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Normalize ASR transcripts via prompt-based cleaner")
    parser.add_argument("--input", default="data/transcripts_raw", help="Input dir with JSONL ASR")
    parser.add_argument("--output", default="data/transcripts_normalized", help="Output dir for normalized JSONL")
    args = parser.parse_args()

    in_dir = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in in_dir.glob("*.jsonl"):
        with p.open("r", encoding="utf-8") as f:
            record = json.loads(f.readline())

        text = record.get("full_text", "")
        norm_text = normalize_text_simple(text)

        record["normalized_text"] = norm_text

        out_path = out_dir / p.name
        with out_path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Normalized transcripts saved to {out_dir}")


if __name__ == "__main__":
    main()

