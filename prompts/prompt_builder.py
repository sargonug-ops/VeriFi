from pathlib import Path
from chunk_adapter import normalize_chunks

PROMPTS_DIR = Path(__file__).parent


def load_system_prompt() -> str:
    return (PROMPTS_DIR / "system_prompt.txt").read_text().strip()


def build_prompt(user_question: str, retrieved_chunks: list[dict]) -> str:
    system_prompt = load_system_prompt()
    chunks = normalize_chunks(retrieved_chunks)

    formatted_chunks = []
    for i, chunk in enumerate(chunks, start=1):
        formatted_chunks.append(
            f"[Source {i}]\n"
            f"Document: {chunk['source_document']}\n"
            f"Page: {chunk['page_number']}\n"
            f"Score: {chunk['score']}\n"
            f"Text: {chunk['text']}"
        )

    context = "\n\n".join(formatted_chunks) if formatted_chunks else "(No chunks retrieved)"

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
If the chunks are not enough, say you could not find enough information.
""".strip()