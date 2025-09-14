import re
from typing import List


def normalize_text_simple(text: str) -> str:
    # Minimal placeholder: collapse spaces, capitalize start.
    t = re.sub(r"\s+", " ", (text or "")).strip()
    if t and not t[0].isupper():
        t = t[0].upper() + t[1:]
    return t


def split_into_chunks_by_words(text: str, size: int = 250) -> List[str]:
    words = (text or "").split()
    chunks = []
    for i in range(0, len(words), size):
        chunk_words = words[i:i+size]
        if chunk_words:
            chunks.append(" ".join(chunk_words))
    return chunks

