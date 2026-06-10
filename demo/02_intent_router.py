import time

from src.clients import client
from src.config import MODEL_NAME, PREMIUM_MODEL
from src.inference import call_model
from src.routing import classify


def process_support_ticket(text: str):
    print(f"\n📥 [New Ticket]: {text[:60]}...")

    t0 = time.time()
    intent = classify(text)
    print(f"🎯 [Router Decision]: {intent} (Took {time.time() - t0:.2f}s)")

    t1 = time.time()

    if "FAST_TRACK" in intent:
        print(f"⚡ Processing on base model ({MODEL_NAME})...")
        res = call_model(
            prompt=text,
            client=client,
            model=MODEL_NAME,
            max_tokens=80,
        )
    else:
        print(f"🧠 Escalating to bigger model ({PREMIUM_MODEL})...")
        res = call_model(
            prompt=text,
            client=client,
            model=PREMIUM_MODEL,
            max_tokens=150,
        )

    reply = res.choices[0].message.content

    print(
        f"✅ Processed in {time.time() - t1:.2f}s "
        f"-> Reply: {reply[:80]}..."
    )

    return reply


if __name__ == "__main__":
    process_support_ticket(
        "Hi, I forgot my account password. Can you send a reset link?"
    )

    process_support_ticket(
        "Your system threw a traceback error: "
        "ZeroDivisionError: division by zero in analytics.py line 42. Fix it."
    )