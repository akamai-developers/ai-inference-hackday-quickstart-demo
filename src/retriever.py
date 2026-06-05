from src.docs import load_docs

def retrieve_docs(question: str, top_k: int = 3) -> list[dict]:
    docs = load_docs()
    question_words = set(question.lower().split())

    scored = []

    for doc in docs:
        text = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
        score = sum(1 for word in question_words if word in text)

        scored.append((score, doc))

    scored.sort(reverse=True, key=lambda item: item[0])

    return [doc for score, doc in scored[:top_k] if score > 0]


def format_context(docs: list[dict]) -> str:
    if not docs:
        return "No relevant docs found."

    chunks = []

    for doc in docs:
        chunks.append(
            f"Title: {doc.get('title')}\n"
            f"Source: {doc.get('url')}\n"
            f"Content: {doc.get('content')}"
        )

    return "\n\n---\n\n".join(chunks)