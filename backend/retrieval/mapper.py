"""Map C++ SearchResult JSON to FastAPI Source objects."""

from typing import Any


def to_sources(raw_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for item in raw_results:
        sources.append(
            {
                "doc": item["source_document"],
                "page": int(item["page_number"]),
                "snippet": item["text"],
                "score": float(item["score"]),
            }
        )
    return sources
