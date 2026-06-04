from config import SMALL_MODEL, LARGE_MODEL


COMPLEX_KEYWORDS = [
    "design",
    "architecture",
    "compare",
    "tradeoff",
    "optimize",
    "latency",
    "scale",
    "reliable",
    "production",
    "fallback",
    "cost",
]


def route_question(question: str) -> dict:
    q = question.lower()

    if len(question.split()) > 20:
        return {
            "model": LARGE_MODEL,
            "reason": "Longer question likely requires deeper reasoning.",
        }

    if any(keyword in q for keyword in COMPLEX_KEYWORDS):
        return {
            "model": LARGE_MODEL,
            "reason": "Question contains architecture/tradeoff language.",
        }

    return {
        "model": SMALL_MODEL,
        "reason": "Simple factual question.",
    }