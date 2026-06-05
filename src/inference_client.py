import time
import httpx
import json
from typing import Generator, Union
from config import BASE_URL, DEFAULT_TIMEOUT_SECONDS

def call_model(
    model: str, 
    messages: list[dict], 
    stream: bool = False,  # 👈 Added this flag
    timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> Generator[dict, None, None]:
    
    start = time.time()
    ttft_ms = None

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 500,
        "stream": stream,  # 👈 Pass the flag to Akamai Cloud
    }

    # CASE A: Standard Non-Streaming (Your Original Code)
    if not stream:
        with httpx.Client() as client:
            response = client.post(BASE_URL, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            latency_ms = round((time.time() - start) * 1000, 2)
            usage = data.get("usage", {})
            
            yield {
                "token": data["choices"][0]["message"]["content"],
                "ttft_ms": latency_ms,  # TTFT equals total latency in non-streaming
                "latency_ms": latency_ms,
                "tokens_in": usage.get("prompt_tokens"),
                "tokens_out": usage.get("completion_tokens"),
            }
            return

    # CASE B: Real-Time Streaming (The New Upgraded Infrastructure)
    with httpx.stream("POST", BASE_URL, json=payload, timeout=timeout) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line or line == "data: [DONE]":
                continue
            if line.startswith("data: "):
                if ttft_ms is None:
                    ttft_ms = round((time.time() - start) * 1000, 2)
                
                chunk_data = json.loads(line[6:])
                delta = chunk_data["choices"].get("delta", {})
                token = delta.get("content", "")
                usage = chunk_data.get("usage", {})
                
                yield {
                    "token": token,
                    "ttft_ms": ttft_ms,
                    "latency_ms": round((time.time() - start) * 1000, 2),
                    "tokens_in": usage.get("prompt_tokens"),
                    "tokens_out": usage.get("completion_tokens"),
                }
