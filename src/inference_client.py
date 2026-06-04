import time
import requests

from config import BASE_URL, DEFAULT_TIMEOUT_SECONDS


def call_model(model: str, messages: list[dict], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
    start = time.time()

    response = requests.post(
        BASE_URL,
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 500,
        },
        timeout=timeout,
    )

    latency_ms = round((time.time() - start) * 1000, 2)
    response.raise_for_status()

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    usage = data.get("usage", {})

    return {
        "answer": answer,
        "latency_ms": latency_ms,
        "tokens_in": usage.get("prompt_tokens"),
        "tokens_out": usage.get("completion_tokens"),
        "raw": data,
    }