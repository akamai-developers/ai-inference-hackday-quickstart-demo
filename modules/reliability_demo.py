from config import LARGE_MODEL
from src.reliability import call_model_with_fallback
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace
from typing import Generator


def run(question: str, stream: bool = False, simulate_failure: bool = False) -> Generator[dict, None, None]:
    # 1. Standard RAG data context lookup
    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    messages = [
        {
            "role": "system",
            "content": "You are a highly resilient assistant. Use the provided context to answer accurately.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    # 2. Pass execution down into our fault-tolerant wrapper
    resilient_generator = call_model_with_fallback(
        primary_model=LARGE_MODEL,
        messages=messages,
        stream=stream,
        simulate_failure=simulate_failure # Passed directly from the Streamlit blackout toggle
    )

    full_answer = ""
    for chunk in resilient_generator:
        # Check if the fallback layer had to intercept a crash
        fallback_active = chunk["fallback_used"]
        model_actually_used = chunk.get("model", LARGE_MODEL if not fallback_active else "SMALL_MODEL")
        
        # Format the text display for the frontend
        token_prefix = "⚠️ [Fallback Active] " if (fallback_active and not full_answer) else ""
        full_answer += chunk["token"]
        
        # Yield the trace dictionary updates step-by-step
        yield {
            "answer": f"{token_prefix}{full_answer}",
            "trace": build_trace(
                module="05 Reliability Layer",
                model=model_actually_used,
                latency_ms=chunk["latency_ms"],
                ttft_ms=chunk["ttft_ms"],
                tokens_in=chunk["tokens_in"],
                tokens_out=chunk["tokens_out"],
                retrieved_docs=[doc["title"] for doc in docs],
                fallback_used=fallback_active,
                errors=[chunk["error_message"]] if fallback_active else []
            ),
        }