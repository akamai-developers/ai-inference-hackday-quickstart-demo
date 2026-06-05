from config import LARGE_MODEL
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace
from typing import Generator  # 👈 Added for type hinting our new stream structure


def run(question: str, stream: bool = False, simulate_failure: bool = False) -> Generator[dict, None, None]:
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

    stream_generator = call_model(LARGE_MODEL, messages, stream=stream)

    full_answer = ""
    
    for chunk in stream_generator:
        full_answer += chunk["token"]
        
        # 👈 Instead of a final return, we yield the updated state to the UI line-by-line
        yield {
            "answer": full_answer,
            "trace": build_trace(
                module="02 Context Optimization",
                model=LARGE_MODEL,
                latency_ms=chunk["latency_ms"],
                ttft_ms=chunk["ttft_ms"],  # 👈 Track our hardware response time metric
                tokens_in=chunk["tokens_in"],
                tokens_out=chunk["tokens_out"],
                retrieved_docs=[doc["title"] for doc in docs],
            ),
        }