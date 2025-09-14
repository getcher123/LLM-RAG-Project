from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions


def get_chroma_collection(persist_dir: str, collection_name: str):
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_or_create_collection(name=collection_name)


def upsert_chunks(collection, model, chunks: List[Dict]):
    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metas = [c.get("metadata", {}) for c in chunks]
    vectors = None
    if model is not None:
        # Pre-compute embeddings to allow custom model usage
        from .embeddings import embed_documents
        vectors = embed_documents(model, texts)
        collection.upsert(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
    else:
        # Or rely on Chroma's built-in embedding fn (not recommended for E5)
        collection.upsert(ids=ids, documents=texts, metadatas=metas)


def query_topk(collection, query_embedding: List[float], k: int = 8) -> List[Dict]:
    res = collection.query(query_embeddings=[query_embedding], n_results=k, include=["documents", "metadatas", "distances"])
    docs = []
    for i in range(len(res["ids"][0])):
        docs.append({
            "id": res["ids"][0][i],
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i],
        })
    return docs

