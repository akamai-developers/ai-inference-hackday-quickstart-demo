import time
import concurrent.futures

from src.inference import call_model
from src.client import client
from src.config import BASE_MODEL, PREMIUM_MODEL


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
    f"Explain concept #{i} in one paragraph."
    for i in range(20)
]


if __name__ == "__main__":
    print("=== TEST 1: SEQUENTIAL REQUESTS ===")
    start = time.time()
    for i, prompt in enumerate(prompts):
        benchmark_request(prompt, i + 1)

    sequential_total = time.time() - start
    print(f"\n Sequential total time: {sequential_total:.2f}s")

    
    print("\n=== TEST 2: SIMULTANEOUS USER REQUESTS ===")
    start = time.time()
    # ThreadpoolExecutor: create X worker threads that can perform tasks simultaneously.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(prompts)) as executor:
        futures = [
            executor.submit(benchmark_request, prompt, i + 1)
            for i, prompt in enumerate(prompts)
        ]
        concurrent.futures.wait(futures)

    concurrent_total = time.time() - start
    speedup = sequential_total / concurrent_total
    requests_per_sec = len(prompts) / concurrent_total

    print(f"\n Concurrent total time: {concurrent_total:.2f}s")
    print(f"🚀 Effective speedup: {speedup:.1f}x")
    print(f" Throughput: {requests_per_sec:.2f} requests/sec")

    print(
        "\n💡 Takeaway: Handling one request at a time is easy. "
        "The real test is what happens when multiple users hit your AI app at the same time. "
        "This is where inference engines like vLLM become valuable: they are designed to serve concurrent traffic efficiently."
    )