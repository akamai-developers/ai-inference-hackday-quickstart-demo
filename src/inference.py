from openai import OpenAI

def call_model(
    prompt: str,
    client: OpenAI,
    model: str,
    max_tokens: int = 100,
    stream: bool = False,
    timeout: float | None = None,
    temperature: float = 0.0
):
    return client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=max_tokens,
        stream=stream,
        timeout=timeout,
        temperature=0
    )