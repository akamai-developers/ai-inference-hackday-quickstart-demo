from openai import OpenAI
from src.config import VLLM_HOST, PREMIUM_HOST

client= OpenAI(
    base_url=VLLM_HOST,
    api_key="dummy"
)

premium = OpenAI(
    base_url=PREMIUM_HOST,
    api_key="dummy"
)