from src.client import client
from src.config import BASE_MODEL
from src.inference import call_model


PREMIUM_KEYWORDS = [
    "debug",
    "outage",
    "root cause",
    "failure chain",
    "mitigation",
    "distributed system",
    "incident",
    "architecture",
    "compliance",
    "security",
    "complex",
]


def clean_route(text: str) -> str:
    text = (text or "").replace("<think>", "").replace("</think>", "").upper()

    if "PREMIUM" in text:
        return "PREMIUM"

    if "BASE" in text:
        return "BASE"

    return "BASE"


def router(request: str) -> str:
    request_lower = request.lower()

    # Demo-friendly deterministic routing
    if any(keyword in request_lower for keyword in PREMIUM_KEYWORDS):
        return "PREMIUM"

    router_prompt = f"""
You are a request router.

Choose which model should handle the user request.

BASE = simple tasks like summarization, definitions, short explanations, classification, or extraction.

PREMIUM = complex tasks like debugging, root cause analysis, multi-step reasoning, architecture analysis, incident analysis, security/legal/financial analysis, or complex coding.

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