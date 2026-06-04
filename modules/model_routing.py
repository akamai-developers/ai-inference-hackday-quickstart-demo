from src.router import route_question
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace


def run(question: str, simulate_failure: bool = False) -> dict:
    route = route_question(question)

    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an Akamai AI Cloud assistant. "
                "Answer using the provided context when useful."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    result = call_model(route["model"], messages)

    return {
        "answer": result["answer"],
        "trace": build_trace(
            module="04 Model Routing",
            model=route["model"],
            route_reason=route["reason"],
            latency_ms=result["latency_ms"],
            tokens_in=result["tokens_in"],
            tokens_out=result["tokens_out"],
            retrieved_docs=[doc["title"] for doc in docs],
        ),
    }