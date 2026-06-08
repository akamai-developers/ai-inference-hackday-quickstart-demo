import os

VLLM_HOST = os.environ.get(
    "VLLM_HOST",
    "http://vllm:8000/v1"
)

MODEL_NAME = os.environ.get(
    "MODEL_NAME",
    "Qwen/Qwen3-8B-FP8"
)

PREMIUM_HOST = os.environ.get(
    "PREMIUM_HOST",
    "http://vllm-premium:8000/v1"  #doesnt exist yet 
)

PREMIUM_MODEL = os.environ.get(
    "PREMIUM_MODEL",
    "Qwen/Qwen3-14B"  
)
  