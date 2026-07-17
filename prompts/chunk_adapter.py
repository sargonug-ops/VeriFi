"""Normalize retrieved chunks from ingestion, vector store, or legacy API shapes."""

CANONICAL_KEYS = ("text", "source_document", "page_number", "score")


def normalize_chunk(chunk: dict) -> dict:
    """Accept ingestion/SearchResult or legacy backend mock fields."""
    return {
        "text": chunk.get("text") or chunk.get("snippet", ""),
        "source_document": chunk.get("source_document") or chunk.get("doc", "Unknown"),
        "page_number": chunk.get("page_number") if chunk.get("page_number") is not None else chunk.get("page", 0),
        "score": float(chunk.get("score", 0.0)),
    }


def normalize_chunks(chunks: list[dict]) -> list[dict]:
    return [normalize_chunk(c) for c in chunks]


def chunks_to_sources(chunks: list[dict]) -> list[dict]:
    """Format for frontend SourceCitation / validator."""
    return [
        {
            "text": c["text"],
            "source_document": c["source_document"],
            "page_number": c["page_number"],
            "score": c["score"],
        }
        for c in chunks
    ]