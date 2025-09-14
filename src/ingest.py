import argparse
import json
from pathlib import Path
from dotenv import load_dotenv

from utils.text_utils import split_into_chunks_by_words
from utils.embeddings import get_embedding_model
from utils.vectorstore import get_chroma_collection, upsert_chunks


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chunk + embed (E5) + insert into ChromaDB")
    parser.add_argument("--input", default="data/transcripts_normalized", help="Dir with normalized JSONL")
    parser.add_argument("--chunks", default="data/chunks", help="Output dir for chunk JSONL")
    parser.add_argument("--db", default="data/chroma_db", help="ChromaDB persist dir")
    parser.add_argument("--collection", default="entertainment", help="Chroma collection name")
    parser.add_argument("--chunk_words", type=int, default=250)
    parser.add_argument("--overlap_sent", type=int, default=2)
    args = parser.parse_args()

    in_dir = Path(args.input)
    chunks_dir = Path(args.chunks)
    chunks_dir.mkdir(parents=True, exist_ok=True)

    model = get_embedding_model("intfloat/multilingual-e5-large-instruct")
    collection = get_chroma_collection(args.db, args.collection)

    all_chunks = []
    for p in in_dir.glob("*.jsonl"):
        with p.open("r", encoding="utf-8") as f:
            record = json.loads(f.readline())
        text = record.get("normalized_text") or record.get("full_text", "")
        source_id = p.stem
        chunks = split_into_chunks_by_words(text, size=args.chunk_words)
        # Minimal metadata
        for i, ch in enumerate(chunks):
            all_chunks.append({
                "id": f"{source_id}::{i}",
                "text": ch,
                "metadata": {"source_id": source_id, "type": "audio"}
            })

    upsert_chunks(collection, model, all_chunks)

    # Save chunks snapshot
    out_path = chunks_dir / "chunks.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for ch in all_chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")

    print(f"Inserted {len(all_chunks)} chunk(s) into Chroma collection '{args.collection}'")


if __name__ == "__main__":
    main()

