def execution_gateway_router(user_prompt: str) -> str:
    """
    Scans intent structure to split simple or conversational queries away from heavy clusters
    """
    heavy_reasoning_signals = ["analyze", "debug", "architect", "optimize", "reason"]
    prompt_lower = user_prompt.lower()
    
    is_complex = any(signal in prompt_lower for signal in heavy_reasoning_signals)
    
    if is_complex or len(user_prompt.split()) > 80:
        return "HIGH_PERFORMANCE_8B_VLLM_CLUSTER"
    return "LIGHTWEIGHT_1B_EDGE_WASM_WORKER"

if __name__ == "__main__":
    print("--- INTELLIGENT COMPUTE ROUTING ENGINE ---")
    query_one = "Hey! Generate a quick motivational tagline for an infrastructure team."
    query_two = "Analyze this core crash dump stack and debug the asynchronous VRAM driver error."
    
    print(f"Prompt 1 Target Destination: {execution_gateway_router(query_one)}")
    print(f"Prompt 2 Target Destination: {execution_gateway_router(query_two)}")