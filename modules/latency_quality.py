from config import SMALL_MODEL, LARGE_MODEL
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context


def run(question: str, simulate_failure: bool = False) -> dict:
    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an Akamai AI Cloud assistant. "
                "Answer clearly and practically using the provided context."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    small = call_model(SMALL_MODEL, messages)
    large = call_model(LARGE_MODEL, messages)

    answer = (
        "### Small model answer\n"
        f"{small['answer']}\n\n"
        "### Large model answer\n"
        f"{large['answer']}"
    )

    return {
        "answer": answer,
        "trace": {
            "module": "03 Latency vs Quality",
            "retrieved_docs": [doc["title"] for doc in docs],
        },
        "comparison": {
            "small_model": {
                "model": SMALL_MODEL,
                "latency_ms": small["latency_ms"],
                "tokens_in": small["tokens_in"],
                "tokens_out": small["tokens_out"],
            },
            "large_model": {
                "model": LARGE_MODEL,
                "latency_ms": large["latency_ms"],
                "tokens_in": large["tokens_in"],
                "tokens_out": large["tokens_out"],
            },
        },
    }