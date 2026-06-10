import time
import concurrent.futures

from src.inference import call_model
from src.clients import client
from src.config import MODEL_NAME, PREMIUM_MODEL


def benchmark_request(prompt: str, req_id: int):
    start = time.time()
    ttft = None
    output_tokens = 0

    stream = call_model(
        prompt=prompt,
        client=client,
        model=PREMIUM_MODEL,
        max_tokens=100,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            if ttft is None:
                ttft = time.time() - start
            output_tokens += 1

    total = time.time() - start
    print(
        f"📊 [User {req_id}] "
        f"TTFT: {ttft:.2f}s | "
        f"Total Time: {total:.2f}s | "
        f"Chunks: {output_tokens}"
    )

    return total


prompts = [
    "Write a quick Python list comprehension.",
    "What is the capital of France?",
    "Explain APIs to a 5-year-old.",
    "How do you declare a variable in Rust?",
]


if __name__ == "__main__":
    print("=== TEST 1: SEQUENTIAL REQUESTS ===")

    start = time.time()
    for i, prompt in enumerate(prompts):
        benchmark_request(prompt, i + 1)

    sequential_total = time.time() - start
    print(f"\n⏱️ Sequential total time: {sequential_total:.2f}s")

    print("\n=== TEST 2: 4 SIMULTANEOUS USER REQUESTS ===")

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(benchmark_request, prompt, i + 1)
            for i, prompt in enumerate(prompts)
        ]
        concurrent.futures.wait(futures)

    concurrent_total = time.time() - start
    print(f"\n⏱️ Concurrent total time: {concurrent_total:.2f}s")

    print(
        "\n💡 Takeaway: Sequential requests make users wait one after another. "
        "Concurrent requests simulate multiple users hitting the same vLLM endpoint, "
        "which is where serving engines like vLLM become valuable."
    )