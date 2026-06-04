from config import LARGE_MODEL
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace


def run(question: str, simulate_failure: bool = False) -> dict:
    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an Akamai AI Cloud documentation assistant. "
                "Use the provided context to answer. If the context is insufficient, say so."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    result = call_model(LARGE_MODEL, messages)

    return {
        "answer": result["answer"],
        "trace": build_trace(
            module="02 Context Optimization",
            model=LARGE_MODEL,
            latency_ms=result["latency_ms"],
            tokens_in=result["tokens_in"],
            tokens_out=result["tokens_out"],
            retrieved_docs=[doc["title"] for doc in docs],
        ),
    }