from openai import OpenAI
from src.config import VLLM_HOST, PREMIUM_HOST

client= OpenAI(
    base_url=VLLM_HOST,
    api_key="dummy"
)

premium_client = OpenAI(
    api_key=PREMIUM_API_KEY
)