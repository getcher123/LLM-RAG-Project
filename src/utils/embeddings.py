from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


def get_embedding_model(model_name: str = "intfloat/multilingual-e5-large-instruct") -> SentenceTransformer:
    return SentenceTransformer(model_name)


def _encode_docs(model: SentenceTransformer, texts: List[str]) -> np.ndarray:
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=False)


def embed_documents(model: SentenceTransformer, texts: List[str]) -> List[List[float]]:
    return _encode_docs(model, [f"passage: {t}" for t in texts]).tolist()


def embed_query(model: SentenceTransformer, query: str) -> List[float]:
    return _encode_docs(model, [f"query: {query}"])[0].tolist()

