from src.clients import client
from src.config import MODEL_NAME
from src.inference import call_model


def classify(ticket: str):

    prompt = f"""
Classify this support ticket.

FAST_TRACK:
- greetings
- refunds
- password resets

COMPLEX_ANALYSIS:
- code bugs
- architecture issues
- data errors

Respond with only one label.

Ticket:
{ticket}
"""

    result = call_model(
        prompt=prompt,
        client=client,
        model=MODEL_NAME,
        max_tokens=10,
        temperature=0
    )

    return result.choices[0].message.content.strip()