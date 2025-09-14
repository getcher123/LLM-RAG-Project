import argparse
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

from utils.embeddings import get_embedding_model, embed_query
from utils.vectorstore import get_chroma_collection, query_topk


def generate_answer(question: str, context_snippets: List[str], model: str = "gpt-4o", temperature: float = 0.3, max_tokens: int = 512) -> str:
    client = OpenAI()
    numbered = "\n".join(f"{i+1}. {c}" for i, c in enumerate(context_snippets))
    system = (
        "Отвечай только на основе предоставленного контекста. Если ответа нет в контексте — скажи, что не знаешь. "
        "Отвечай кратко и структурировано."
    )
    user = f"Вопрос: {question}\n\nКонтекст (нумерованный список сниппетов):\n{numbered}"
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def answer(question: str, db_path: str, collection: str, k: int = 8) -> Dict:
    emb = get_embedding_model("intfloat/multilingual-e5-large-instruct")
    coll = get_chroma_collection(db_path, collection)
    q_vec = embed_query(emb, question)
    docs = query_topk(coll, q_vec, k=k)
    snippets = [d["text"] for d in docs]
    reply = generate_answer(question, snippets)
    return {"answer": reply, "contexts": docs}


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Simple RAG query runner")
    parser.add_argument("--db", default="data/chroma_db")
    parser.add_argument("--collection", default="entertainment")
    parser.add_argument("--question", required=True)
    parser.add_argument("--k", type=int, default=8)
    args = parser.parse_args()

    result = answer(args.question, args.db, args.collection, args.k)
    print(result["answer"]) 


if __name__ == "__main__":
    main()

