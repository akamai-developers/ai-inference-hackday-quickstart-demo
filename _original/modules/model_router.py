from config import LARGE_MODEL
from src.router import route_question
from src.inference_client import call_model
from src.retriever import retrieve_docs, format_context
from src.metrics import build_trace
from typing import Generator


def run(question: str, stream: bool = False, simulate_failure: bool = False) -> Generator[dict, None, None]:
    # 1. Hand the prompt over to the routing layer to pick our target model
    route_result = route_question(question)
    selected_model = route_result["model"]
    reason = route_result["reason"]
    
    module_label = "04 Smart Routing (Large)" if selected_model == LARGE_MODEL else "04 Smart Routing (Small)"

    # 2. Extract documentation context (standard RAG flow)
    docs = retrieve_docs(question, top_k=3)
    context = format_context(docs)

    messages = [
        {
            "role": "system",
            "content": "Use the provided context to answer. Be concise and match your depth to the complexity of the request.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    # 3. Stream the output of the dynamically chosen hardware tier
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
                route_reason=reason  # 👈 Pass the dynamic text block directly into the UI dashboard
            ),
        }