import time
import httpx
import json
from typing import Generator, Union
from config import LARGE_MODEL, LARGE_MODEL_URL, SMALL_MODEL_URL, DEFAULT_TIMEOUT_SECONDS


def call_model(
    model: str, 
    messages: list[dict], 
    stream: bool = False,
    timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> Generator[dict, None, None]:
    
    start = time.time()
    ttft_ms = None

    # 👈 INFRASTRUCTURE ROUTING INTERCEPT: Choose target port endpoint
    target_url = LARGE_MODEL_URL if model == LARGE_MODEL else SMALL_MODEL_URL

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 500,
        "stream": stream, 
    }

    # CASE A: Standard Non-Streaming
    if not stream:
        with httpx.Client() as client:
            response = client.post(target_url, json=payload, timeout=timeout)
            response.raise_for_status() # Will raise an error for non-2xx responses, which can be caught by the reliability layer
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

    # CASE B: Real-Time Streaming
    with httpx.stream("POST", target_url, json=payload, timeout=timeout) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line or line == "data: [DONE]":
                continue
            if line.startswith("data: "):
                if ttft_ms is None:
                    ttft_ms = round((time.time() - start) * 1000, 2)
                
                chunk_data = json.loads(line[6:])
                
                # 👇 FIX: Add [0] here to extract the dictionary out of the choices list
                if "choices" in chunk_data and chunk_data["choices"]:
                    choice = chunk_data["choices"][0]
                    delta = choice.get("delta", {})
                    token = delta.get("content", "")
                else:
                    token = ""
                    
                usage = chunk_data.get("usage", {})
                
                yield {
                    "token": token,
                    "ttft_ms": ttft_ms,
                    "latency_ms": round((time.time() - start) * 1000, 2),
                    "tokens_in": usage.get("prompt_tokens") if usage else 0,
                    "tokens_out": usage.get("completion_tokens") if usage else 0,
                }