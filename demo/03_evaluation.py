from src.inference import call_model
from src.client import client
from src.config import BASE_MODEL, PREMIUM_MODEL


def clean_output(text: str) -> str:
    return text.replace("<think>", "").replace("</think>", "").strip()


def generate_response(user_prompt: str, model: str) -> str:
    result = call_model(
        prompt=user_prompt,
        client=client,
        model=model,
        max_tokens=150,
        temperature=0,
    )

    return clean_output(result.choices[0].message.content)


def evaluate_responses(
    user_prompt: str,
    small_output: str,
    large_output: str,
) -> str:
    print("🔍 [LLM Judge] Comparing outputs...")

    eval_prompt = f"""
You are an expert AI evaluator.

Compare the following two responses to the user's request.

User Request:
{user_prompt}

Response A (Smaller Model):
{small_output}

Response B (Larger Model):
{large_output}

Evaluate each response on:

- Accuracy (1-10)
- Completeness (1-10)
- Clarity (1-10)

Then answer:

1. Which response is better?
2. Is the quality difference significant?
3. Could Response A be acceptable in a production application?

Return your answer in the following format:

Response A
- Accuracy:
- Completeness:
- Clarity:

Response B
- Accuracy:
- Completeness:
- Clarity:

Winner:
Reasoning:
Production Verdict:
"""

    eval_res = call_model(
        prompt=eval_prompt,
        client=client,
        model=PREMIUM_MODEL,
        max_tokens=300,
        temperature=0,
    )

    return clean_output(eval_res.choices[0].message.content)


if __name__ == "__main__":
    print("=== MODEL COMPARISON + LLM JUDGE ===")

    user_prompt = (
        "Explain speculative decoding and why it improves inference performance."
    )

    print(f"\n📥 User Request:\n{user_prompt}")

    # Smaller model
    small_output = generate_response(
        user_prompt,
        BASE_MODEL,
    )

    # Larger model
    large_output = generate_response(
        user_prompt,
        PREMIUM_MODEL,
    )

    print("\n==============================")
    print("🤖 SMALL MODEL OUTPUT")
    print("==============================")
    print(small_output)

    print("\n==============================")
    print("🚀 LARGE MODEL OUTPUT")
    print("==============================")
    print(large_output)

    verdict = evaluate_responses(
        user_prompt,
        small_output,
        large_output,
    )

    print("\n==============================")
    print("📋 LLM JUDGE EVALUATION")
    print("==============================")
    print(verdict)