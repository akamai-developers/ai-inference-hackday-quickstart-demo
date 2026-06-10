from src.inference import call_model
from src.client import client
from src.config import BASE_MODEL, PREMIUM_MODEL


def clean_output(text: str) -> str:
    return text.replace("<think>", "").replace("</think>", "").strip()


def generate_response(user_prompt: str) -> str:
    print("🤖 [Generation] Calling base model...")

    result = call_model(
        prompt=user_prompt,
        client=client,
        model=BASE_MODEL,
        max_tokens=120,
        temperature=0,
    )

    return clean_output(result.choices[0].message.content)


def evaluate_response(user_prompt: str, output: str) -> str:
    print("🔍 [Automated Eval] Running lightweight quality check...")

    eval_prompt = f"""
You are evaluating an AI assistant response.

Check whether the response:
- answers the user's request
- is clear and helpful
- is professional

Answer with only PASS or FAIL.

User request:
{user_prompt}

AI response:
{output}
"""

    eval_res = call_model(
        prompt=eval_prompt,
        client=client,
        model=PREMIUM_MODEL,
        max_tokens=10,
        temperature=0,
    )

    return clean_output(eval_res.choices[0].message.content)


if __name__ == "__main__":
    print("=== MODULE 3: LIGHTWEIGHT EVALUATION ===")

    user_prompt = (
        "Explain what vLLM is in two sentences for a software engineer."
    )

    print(f"\n📥 User Request: {user_prompt}")

    output = generate_response(user_prompt)

    print(f"\n💬 Model Output:\n{output}")

    verdict = evaluate_response(user_prompt, output)

    print(f"\n📋 Quality Check: {verdict}")