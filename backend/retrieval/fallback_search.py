"""Python fallback search when search_cli is unavailable (Chris's VectorStore WIP).

Reads chunks.jsonl and performs cosine similarity in Python so the API bridge
can be tested end-to-end before the C++ store is complete. Once search_cli
builds and runs, vector_client.search() takes precedence.
"""

import json
import math
from pathlib import Path
from typing import Any

from .config import CHUNKS_PATH


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / (mag_a * mag_b)


def _load_chunks(path: Path) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def search(embedding: list[float], top_k: int = 5) -> list[dict[str, Any]]:
    if not CHUNKS_PATH.is_file():
        raise FileNotFoundError(f"chunks file not found at {CHUNKS_PATH}")

    chunks = _load_chunks(CHUNKS_PATH)
    scored: list[tuple[float, dict[str, Any]]] = []

    for chunk in chunks:
        chunk_embedding = chunk.get("embedding", [])
        if len(chunk_embedding) != len(embedding):
            continue
        score = _cosine_similarity(embedding, chunk_embedding)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    limit = min(top_k, len(scored))

    results: list[dict[str, Any]] = []
    for score, chunk in scored[:limit]:
        results.append(
            {
                "score": score,
                "text": chunk["text"],
                "source_document": chunk["source_document"],
                "page_number": chunk["page_number"],
            }
        )
    return results
