import math

def calculate_gpu_requirements():
    print("=" * 50)
    print("        HACKATHON AI HARDWARE CALCULATOR        ")
    print("=" * 50)
    
    # 1. User Inputs
    param_input = input("Enter model parameter size in Billions (e.g., 7, 14, 70): ")
    params = float(param_input)
    
    print("\nSelect Precision / Quantization Level:")
    print(" 1. 4-bit Quantized (Highly Recommended for Hackathons)")
    print(" 2. 8-bit Quantized (Good balance)")
    print(" 3. 16-bit Full Precision (FP16 / Unquantized)")
    
    choice = input("Enter choice (1-3): ")
    bits = 4 if choice == "1" else 8 if choice == "2" else 16
    
    context_input = input("\nExpected max context length in tokens (default 2048): ")
    context = int(context_input) if context_input.strip() else 2048

    # 2. Math Calculations
    weight_gb = (params * bits) / 8
    
    # KV Cache approximation: accounts for context memory scaling per billion parameters
    kv_cache_gb = (params * 0.1) * (context / 1024)
    cuda_overhead_gb = 1.5 
    
    total_vram_needed = weight_gb + kv_cache_gb + cuda_overhead_gb
    safe_target = math.ceil(total_vram_needed)

    # 3. Output Recommendations
    print("\n" + "-" * 50)
    print(f" RESULTS FOR A {params}B MODEL AT {bits}-BIT PREVISION")
    print("-" * 50)
    print(f" -> Pure Model Weight Size: {weight_gb:.2f} GB")
    print(f" -> Context (KV Cache) Size: {kv_cache_gb:.2f} GB")
    print(f" -> System & CUDA Overhead:  {cuda_overhead_gb:.2f} GB")
    print(f" -> MINIMUM TOTAL VRAM REQUIRED: {total_vram_needed:.2f} GB")
    print(f" -> TARGET GPU SIZE RECOMMENDED: {safe_target} GB or higher")
    print("-" * 50)
    
    # Hardware matching logic
    print(" MATCHING HARDWARE RECOMMENDATIONS:")
    if safe_target <= 8:
        print("   * Local: Most consumer laptops or standard gaming GPUs (RTX 3060/4060).")
        print("   * Cloud: Ultra-budget instances like an NVIDIA T4.")
    elif safe_target <= 16:
        print("   * Local: Apple Silicon Mac (16GB+ Unified Memory) or RTX 4080.")
        print("   * Cloud: Cost-effective mid-tier options like an NVIDIA A10G.")
    elif safe_target <= 24:
        print("   * Local: High-end desktop GPU with deep VRAM (RTX 3090 / RTX 4090).")
        print("   * Cloud: NVIDIA A10G or a fraction of an A100.")
    elif safe_target <= 80:
        print("   * Local: Highly unlikely for standard laptops. Requires multi-GPU desktops.")
        print("   * Cloud: Dedicated enterprise cloud servers like 1x NVIDIA A100 (80GB).")
    else:
        print("   * Warning: Extreme workload. You will need an 8x H100 cluster or heavy quantization.")
    print("=" * 50)

if __name__ == "__main__":
    calculate_gpu_requirements()