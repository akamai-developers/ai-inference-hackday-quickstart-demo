from openai import OpenAI
import os

client = OpenAI(
    base_url="http://agentgateway:8080/v1",
    api_key=os.getenv("VLLM_API_KEY")
)