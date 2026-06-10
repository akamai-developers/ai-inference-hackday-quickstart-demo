import time

from src.client import client
from src.config import BASE_MODEL, PREMIUM_MODEL
from src.inference import call_model
from src.routing import router


def route_and_infer(user_request: str):
    print(f"\n[User Request]: {user_request[:100]}...")

    t0 = time.time()
    route = router(user_request)

    print(f"[Router Decision]: {route} (Took {time.time() - t0:.2f}s)")

    if route == "BASE":
        selected_model = BASE_MODEL
        max_tokens = 80
    else:
        selected_model = PREMIUM_MODEL
        max_tokens = 180

    print(f"[Selected Model]: {selected_model}")

    t1 = time.time()

    result = call_model(
        prompt=user_request,
        client=client,
        model=selected_model,
        max_tokens=max_tokens,
        temperature=0,
    )

    reply = result.choices[0].message.content or "[EMPTY RESPONSE]"

    print(
        f"✅ Completed with {selected_model} "
        f"in {time.time() - t1:.2f}s "
        f"-> Reply: {reply[:120]}..."
    )

    return reply


if __name__ == "__main__":
    route_and_infer(
        "Summarize Kubernetes in one sentence."
    )

    route_and_infer(
        "Analyze this distributed system outage: requests are timing out across three services, database CPU is high, and retries are causing cascading failures. Identify likely root causes and mitigation steps."
    )