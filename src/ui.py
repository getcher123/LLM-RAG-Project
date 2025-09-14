import gradio as gr
from dotenv import load_dotenv

from utils.embeddings import get_embedding_model, embed_query
from utils.vectorstore import get_chroma_collection, query_topk
from serve import generate_answer


def build_app(db_path: str = "data/chroma_db", collection: str = "entertainment"):
    emb = get_embedding_model("intfloat/multilingual-e5-large-instruct")
    coll = get_chroma_collection(db_path, collection)

    def respond(question: str):
        q_vec = embed_query(emb, question)
        docs = query_topk(coll, q_vec, k=8)
        snippets = [d["text"] for d in docs]
        ans = generate_answer(question, snippets)
        sources = "\n".join(f"- {d.get('metadata', {}).get('source_id', 'doc')}" for d in docs)
        return ans, sources

    with gr.Blocks() as demo:
        gr.Markdown("# RAG-чатбот по индустрии развлечений")
        with gr.Row():
            inp = gr.Textbox(label="Ваш вопрос", placeholder="Кто режиссёр ... ?")
        with gr.Row():
            out = gr.Markdown(label="Ответ")
        with gr.Row():
            src = gr.Markdown(label="Использованные источники")
        btn = gr.Button("Спросить")
        btn.click(fn=respond, inputs=inp, outputs=[out, src])
    return demo


if __name__ == "__main__":
    load_dotenv()
    app = build_app()
    app.launch()

