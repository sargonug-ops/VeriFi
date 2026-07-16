"""VeriFi RAG: chunks + question -> grounded answer + citations."""

from chunk_adapter import normalize_chunks, chunks_to_sources
from prompt_builder import build_prompt
from llm_client import call_llm

INSUFFICIENT_MSG = (
    "I could not find enough information in the provided documents to answer this confidently."
)


def generate_rag_response(user_question: str, retrieved_chunks: list[dict]) -> dict:
    """
    Returns:
        {"answer": str, "sources": list[dict]}
    Sources use: text, source_document, page_number, score
    """
    question = (user_question or "").strip()
    if not question:
        return {
            "answer": "Please enter a valid question.",
            "sources": [],
        }

    chunks = normalize_chunks(retrieved_chunks)

    if not chunks:
        return {
            "answer": INSUFFICIENT_MSG,
            "sources": [],
        }

    prompt = build_prompt(question, chunks)
    answer = call_llm(prompt).strip() or INSUFFICIENT_MSG

    return {
        "answer": answer,
        "sources": chunks_to_sources(chunks),
    }