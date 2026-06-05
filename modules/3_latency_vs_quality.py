from config import LARGE_MODEL, SMALL_MODEL  # 👈 Ensure SMALL_MODEL is defined in your config
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace
from typing import Generator

def run(question: str, use_large_model: bool = True, stream: bool = False, simulate_failure: bool = False) -> Generator[dict, None, None]:
    # 1. Fetch relevant documentation exactly like Module 2
    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    # 2. Select the model dynamically based on the UI toggle
    selected_model = LARGE_MODEL if use_large_model else SMALL_MODEL
    module_label = "03 Latency vs Quality (Large)" if use_large_model else "03 Latency vs Quality (Small)"

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

    # 3. Execute the call using the selected model and the stream toggle
    stream_generator = call_model(selected_model, messages, stream=stream)

    full_answer = ""
    for chunk in stream_generator:
        full_answer += chunk["token"]
        
        yield {
            "answer": full_answer,
            "trace": build_trace(
                module=module_label,
                model=selected_model,
                latency_ms=chunk["latency_ms"],
                ttft_ms=chunk["ttft_ms"],
                tokens_in=chunk["tokens_in"],
                tokens_out=chunk["tokens_out"],
                retrieved_docs=[doc["title"] for doc in docs],
            ),
        }