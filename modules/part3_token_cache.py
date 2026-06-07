import time
from src.mock_data import MOCK_15K_TOKEN_CONTEXT, mock_semantic_cache_lookup
from src.telemetry import track_metrics

@track_metrics("Inference Router Processing Phase")
def simulate_gateway_intercept(prompt: str, bypass_cache: bool, bloat_context: bool):
    # 1. Edge Layer: Semantic Cache Lookup
    if not bypass_cache:
        hit = mock_semantic_cache_lookup(prompt)
        if hit:
            print(f"🎯 [GATEWAY INTERCEPT: CACHE HIT] Served from localized cache memory.")
            print(f"   Response Payload: {hit}")
            return
            
    # 2. Compute Layer: Processing network forwarding simulation
    if bloat_context:
        print("💸 [CACHE MISS] Processing bloated RAG prompt context data package (15k tokens)...")
        time.sleep(1.4) # Simulate input processing overhead delay
    else:
        print("⚡ [CACHE MISS] Forwarding optimized minimal text vector payload...")
        time.sleep(0.15)

if __name__ == "__main__":
    print("--- SYSTEM COST REDUCTION DEMO ---")
    print("Scenario A (Bloated Payload):")
    simulate_gateway_intercept("How do I clear my GPU memory cache?", bypass_cache=True, bloat_context=True)
    
    print("Scenario B (Optimized Context Layer):")
    simulate_gateway_intercept("How do I clear my GPU memory cache?", bypass_cache=True, bloat_context=False)
    
    print("Scenario C (Semantic Database Cache Hit):")
    simulate_gateway_intercept("Can you show me how to clear GPU memory?", bypass_cache=False, bloat_context=False)