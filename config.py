import os

# Base cluster endpoints pre-configured in the workshop environment
VLLM_URL = os.getenv("VLLM_CLUSTER_URL", "http://localhost:8000")
OLLAMA_URL = os.getenv("OLLAMA_DEV_URL", "http://localhost:11434")