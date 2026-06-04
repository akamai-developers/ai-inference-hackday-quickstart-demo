from config import LARGE_MODEL
from src.inference_client import call_model
from src.metrics import build_trace


def run(question: str, simulate_failure: bool = False) -> dict:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant answering questions about Akamai AI Cloud.",
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    result = call_model(LARGE_MODEL, messages)

    return {
        "answer": result["answer"],
        "trace": build_trace(
            module="01 Baseline",
            model=LARGE_MODEL,
            latency_ms=result["latency_ms"],
            tokens_in=result["tokens_in"],
            tokens_out=result["tokens_out"],
        ),
    }