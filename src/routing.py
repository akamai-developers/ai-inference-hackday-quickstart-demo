from src.client import client
from src.config import BASE_MODEL
from src.inference import call_model


def clean_route(text: str) -> str:
    text = (text or "").replace("<think>", "").replace("</think>", "").upper()

    if "PREMIUM" in text:
        return "PREMIUM"

    return "BASE"


def router(request: str) -> str:
    router_prompt = f"""
You are a request router.

Choose which model should handle the user request.

BASE = simple tasks like:
- summarization
- definitions
- short explanations
- classification
- extraction

PREMIUM = complex tasks like:
- debugging
- multi-step reasoning
- architecture analysis
- incident/outage analysis
- security/legal/financial analysis
- complex coding

User request:
{request}

Return only one word: BASE or PREMIUM.
"""

    result = call_model(
        prompt=router_prompt,
        client=client,
        model=BASE_MODEL,
        max_tokens=10,
        temperature=0,
    )

    return clean_route(result.choices[0].message.content)