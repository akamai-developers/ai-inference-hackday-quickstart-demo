import os

BASE_URL = os.getenv("AKAMAI_INFERENCE_URL", "http://localhost:8000/v1/chat/completions")

SMALL_MODEL = os.getenv("SMALL_MODEL", "small-model")
LARGE_MODEL = os.getenv("LARGE_MODEL", "large-model")

DEFAULT_TIMEOUT_SECONDS = 30