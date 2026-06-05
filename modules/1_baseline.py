from config import LARGE_MODEL
from src.inference_client import call_model
from src.metrics import build_trace
from typing import Generator

def run(question: str, stream: bool = False, simulate_failure: bool = False) -> Generator[dict, None, None]:
    messages = [
        {"role": "system", "content": "You are a helpful assistant answering questions about Akamai AI Cloud."},
        {"role": "user", "content": question},
    ]

    # Pass the streaming flag down to the client
    stream_generator = call_model(LARGE_MODEL, messages, stream=stream)
    
    full_answer = ""
    for chunk in stream_generator:
        full_answer += chunk["token"]
        yield {
            "answer": full_answer,
            "trace": build_trace(
                module="01 Baseline",
                model=LARGE_MODEL,
                latency_ms=chunk["latency_ms"],
                ttft_ms=chunk["ttft_ms"],
                tokens_in=chunk["tokens_in"],
                tokens_out=chunk["tokens_out"],
            ),
        }
