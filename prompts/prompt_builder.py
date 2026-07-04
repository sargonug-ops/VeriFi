from pathlib import Path


PROMPTS_DIR = Path(__file__).parent


def load_system_prompt() -> str:
    """Load VeriFi's system prompt from the prompts folder."""
    return (PROMPTS_DIR / "system_prompt.txt").read_text().strip()


def build_prompt(user_question: str, retrieved_chunks: list[dict]) -> str:
    """
    Build the final prompt sent to the LLM.

    This keeps the user's question, retrieved document chunks,
    and system prompt in one consistent format.
    """
    system_prompt = load_system_prompt()

    formatted_chunks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        formatted_chunks.append(
            f"[Source {i}]\n"
            f"Document: {chunk.get('doc', 'Unknown')}\n"
            f"Page: {chunk.get('page', 'Unknown')}\n"
            f"Score: {chunk.get('score', 'N/A')}\n"
            f"Text: {chunk.get('snippet', '')}"
        )

    context = "\n\n".join(formatted_chunks)

    return f"""
SYSTEM PROMPT:
{system_prompt}

USER QUESTION:
{user_question}

RETRIEVED DOCUMENT CHUNKS:
{context}

TASK:
Answer the user question using only the retrieved document chunks.
Include citations from the sources above.
""".strip()