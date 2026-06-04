from src.router import route_question
from src.reliability import call_with_retry_and_fallback
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
                "Answer using the provided context. Be practical and specific."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    result = call_with_retry_and_fallback(
        primary_model=route["model"],
        messages=messages,
        simulate_failure=simulate_failure,
        retries=1,
    )

    model_used = result.get("fallback_model", route["model"])

    trace = build_trace(
        module="06 Observability",
        model=model_used,
        route_reason=route["reason"],
        latency_ms=result["latency_ms"],
        tokens_in=result["tokens_in"],
        tokens_out=result["tokens_out"],
        retrieved_docs=[
            {
                "title": doc["title"],
                "url": doc.get("url"),
            }
            for doc in docs
        ],
        fallback_used=result["fallback_used"],
        errors=result["errors"],
    )

    trace["inference_path"] = [
        "receive_question",
        "retrieve_relevant_docs",
        "route_to_model",
        "call_model_with_retry",
        "fallback_if_needed",
        "return_answer_and_metrics",
    ]

    return {
        "answer": result["answer"],
        "trace": trace,
    }