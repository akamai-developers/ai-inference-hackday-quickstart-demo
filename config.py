# The underlying physical endpoints listening on your Akamai Cloud VM
LARGE_MODEL_URL = "http://172.232.238.91:8000/v1/chat/completions"
SMALL_MODEL_URL = "http://172.232.238.91:8001/v1/chat/completions"

# Model identifier definitions used to build the metadata trace
LARGE_MODEL = "meta-llama/Meta-Llama-3-70B-Instruct"
SMALL_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct-AWQ"

DEFAULT_TIMEOUT_SECONDS = 30