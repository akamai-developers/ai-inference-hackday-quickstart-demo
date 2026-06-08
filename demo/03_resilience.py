import time

from src.clients import client, premium_client
from src.config import MODEL_NAME, PREMIUM_MODEL
from src.inference import call_model


# You will run it once to show a perfect run with metrics, then 
# INTENTIONAL FIX/BREAK TARGET FOR LIVE DEMO:
# Change port '8000' to '9999' live on stage to simulate a cluster crash!
def resilient_call(prompt: str, timeout: float = 3.0):
    print("\n🚀 [Processing Request] Calling Primary Engine...")

    start_time = time.time()

    try:
        response = call_model(
            prompt=prompt,
            client=client,
            model=MODEL_NAME,
            max_tokens=100,
            timeout=timeout,
        )

        latency = time.time() - start_time
        output = response.choices[0].message.content

        print(f"✅ [SUCCESS] Primary Akamai vLLM responded in {latency:.2f}s")

        return {
            "source": "PRIMARY",
            "output": output,
            "latency": latency,
            "fallback_used": False,
            "error": None,
        }

    except Exception as e:
        print(f"🚨 [CRITICAL OUTAGE] Primary Engine Failed! Reason: {e}")
        print("🛡️ [CIRCUIT BREAKER] Diverting traffic to fallback model...")

        fallback_start = time.time()

        response = call_model(
            prompt=prompt,
            client=premium_client,
            model=PREMIUM_MODEL,
            max_tokens=100,
        )

        fallback_latency = time.time() - fallback_start
        output = response.choices[0].message.content

        print(
            f"🛡️ [FALLBACK SUCCESS] Fulfilled via fallback in "
            f"{fallback_latency:.2f}s"
        )

        return {
            "source": "FALLBACK",
            "output": output,
            "latency": fallback_latency,
            "fallback_used": True,
            "error": str(e),
        }


if __name__ == "__main__":
    print("=== MODULE 3: RELIABILITY WITH FALLBACK ===")

    result = resilient_call(
        "Generate a friendly welcome message for our platform."
    )

    print(f"🧭 Served by: {result['source']}")
    print(f"⏱️ Latency: {result['latency']:.2f}s")
    print(f"💬 Output: {result['output']}")