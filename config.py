import os


# 1. Point this to your vLLM Big Model chat completions endpoint
BASE_URL = os.getenv("AKAMAI_INFERENCE_URL", "http://172.232.238.91:8000/v1/chat/completions")

# 2. Update these to the exact strings your vLLM servers are hosting
LARGE_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
SMALL_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

DEFAULT_TIMEOUT_SECONDS = 30