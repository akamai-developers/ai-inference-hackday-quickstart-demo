from src.inference_client import call_model
from config import SMALL_MODEL


def call_with_retry_and_fallback(
    primary_model: str,
    messages: list[dict],
    simulate_failure: bool = False,
    retries: int = 1,
) -> dict:
    errors = []

    for attempt in range(retries + 1):
        try:
            if simulate_failure:
                raise RuntimeError("Simulated primary model failure")

            result = call_model(primary_model, messages)
            result["fallback_used"] = False
            result["errors"] = errors
            return result

        except Exception as e:
            errors.append(f"Attempt {attempt + 1}: {str(e)}")

    fallback_result = call_model(SMALL_MODEL, messages)
    fallback_result["fallback_used"] = True
    fallback_result["errors"] = errors
    fallback_result["fallback_model"] = SMALL_MODEL

    return fallback_result