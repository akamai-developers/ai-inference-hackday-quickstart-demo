from src.resilience import resilient_call
from src.inference import call_model
from src.clients import premium
from src.config import PREMIUM_MODEL


def evaluate_response(output: str):
    print("🔍 [Automated Eval] Running rapid accuracy check...")

    eval_prompt = (
        "Is the following AI response polite and professional? "
        "Answer with only YES or NO.\n"
        f"Response: '{output}'"
    )

    eval_res = call_model(
        prompt=eval_prompt,
        client=premium,
        model=PREMIUM_MODEL,
        max_tokens=5,
    )

    return eval_res.choices[0].message.content.strip()


if __name__ == "__main__":
    print("=== MODULE 4: LIGHTWEIGHT EVALUATION ===")

    result = resilient_call(
        "Generate a friendly welcome message for our platform."
    )

    print(f"🧭 Served by: {result['source']}")
    print(f"💬 Output: {result['output']}")

    verdict = evaluate_response(result["output"])

    print(f"📋 Professional tone: {verdict}")