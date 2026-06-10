from src.client import client
from src.config import BASE_MODEL
from src.inference import call_model


def router(request: str):
    prompt = f"""
You are a routing classifier.

Classify the request into one category.

FAST_TRACK:
- simple summaries
- greetings
- rewrites
- straightforward factual questions

COMPLEX_ANALYSIS:
- debugging
- architecture analysis
- multi-step reasoning
- performance issues
- system design tradeoffs
- data analysis

IMPORTANT:
Output ONLY one label.
Do not explain.
Do not think aloud.
Do not output any other text.

Request:
{request}
"""
    result = call_model(
        prompt=prompt,
        client=client,
        model=BASE_MODEL,
        max_tokens=10,
        temperature=0,
    )

    return result.choices[0].message.content.strip()