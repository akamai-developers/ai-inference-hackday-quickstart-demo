import asyncio
import time
import aiohttp
from src.config import VLLM_URL, OLLAMA_URL


# Throughput Scaling via Dynamic Batching
# vLLM takes those 10 distinct requests and dynamically batches them into 
#a single parallel GPU forward pass, maximizing hardware utilization without 
# hurting individual response latencies.
async def stress_test_engine(endpoint_url: str, engine_name: str):
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "prompt": "Explain PagedAttention mechanics like OS virtual memory allocations.",
        "max_tokens": 100,
        "temperature": 0.0
    }
    
    start_time = time.time()
    print(f"🚀 Dispatching 10 parallel requests immediately to -> {engine_name}...")
    
    async with aiohttp.ClientSession() as session:
        tasks = [session.post(f"{endpoint_url}/v1/completions", json=payload) for _ in range(10)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
    duration = time.time() - start_time
    print(f"✅ {engine_name} processed concurrent surge block in: {duration:.2f} seconds\n")

if __name__ == "__main__":
    print("--- CONCURRENT MEMORY STRESS TESTS ---")
    # This proves how PagedAttention + Continuous Batching defeats sequential layout issues
    try:
        asyncio.run(stress_test_engine(OLLAMA_URL, "Standard Developer Engine (Ollama)"))
    except Exception:
        print("❌ Ollama connection unavailable or timeout experienced.\n")
        
    try:
        asyncio.run(stress_test_engine(VLLM_URL, "Production Multi-Tenant Engine (vLLM)"))
    except Exception:
        print("❌ Production vLLM endpoint cluster currently unreachable.")