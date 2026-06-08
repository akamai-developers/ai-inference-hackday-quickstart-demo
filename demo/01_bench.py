import time 
from src.inference import call_model
from src.clients import client
from src.config import MODEL_NAME
import concurrent.futures


# Module 1: The Raw Infrastructure Benchmark
# Showcases how the shared Akamai LKE cluster handles multiple simultaneous hacker requests compared to sequential processing.
def benchmark_request(prompt: str, req_id: int):
    start = time.time()
    ttft = None

    stream = call_model(
        prompt=prompt,
        client=client,
        model=MODEL_NAME,
        max_tokens=100,
        stream=True, # Streaming is required to capture TTFT!
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            if ttft is None:
                ttft = time.time() - start

    total = time.time() - start
    print(f"📊 [User {req_id}] TTFT: {ttft:.2f}s | Total Generation Time: {total:.2f}s")


if __name__ == "__main__":
    print("=== TEST 1: SIMULATING 4 SIMULTANEOUS USER REQUESTS ===")

    prompts = [
        "Write a quick Python list comprehension.",
        "What is the capital of France?",
        "Explain APIs to a 5-year-old.",
        "How do you declare a variable in Rust?"
    ]

    start_batch = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(benchmark_request, p,i + 1)
            for i, p in enumerate(prompts)
        ]
        concurrent.futures.wait(futures)

    print(
        f"\n⏱️ All requests completed concurrently in: "
        f"{time.time() - start_batch:.2f}s"
    )

    print(
        "💡 Notice how the times overlap? "
        "That is vLLM's Continuous Batching in action!"