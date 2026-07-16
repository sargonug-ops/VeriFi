"""Embed user queries with the same model used during ingestion."""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_query(query: str) -> list[float]:
    model = _get_model()
    vector = model.encode(query, convert_to_numpy=True)
    return vector.tolist()
