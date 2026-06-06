import json
from pathlib import Path

DOCS_PATH = Path("data/docs.jsonl")


def load_docs():
    docs = []

    if not DOCS_PATH.exists():
        return docs

    with DOCS_PATH.open("r") as f:
        for line in f:
            docs.append(json.loads(line))

    return docs