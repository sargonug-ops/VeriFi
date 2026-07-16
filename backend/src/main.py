"""
VeriFi Backend - FastAPI server
API bridge: embeds queries, searches vector store, returns sources to frontend.

Run with:
    cd backend/src
    uvicorn main:app --reload --port 8000
"""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Allow imports from backend/retrieval when running from backend/src/
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from retrieval import embedder, fallback_search, mapper, vector_client  # noqa: E402
from retrieval.config import CHUNKS_PATH, SEARCH_CLI_PATH  # noqa: E402

logger = logging.getLogger(__name__)

_retrieval_ready = False
_use_cpp_cli = False


def _check_retrieval_ready() -> tuple[bool, bool]:
    chunks_ok = CHUNKS_PATH.is_file()
    cli_ok = vector_client.is_cli_available()
    return chunks_ok, cli_ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _retrieval_ready, _use_cpp_cli

    chunks_ok, cli_ok = _check_retrieval_ready()
    _retrieval_ready = chunks_ok
    _use_cpp_cli = cli_ok

    if cli_ok:
        logger.info("Retrieval ready via C++ search_cli at %s", SEARCH_CLI_PATH)
    elif chunks_ok:
        logger.warning(
            "search_cli unavailable — using Python fallback until Chris's "
            "VectorStore compiles. Build with task 'Build search_cli'."
        )
    else:
        logger.warning("Retrieval degraded: missing %s", CHUNKS_PATH)

    yield


app = FastAPI(
    title="VeriFi API",
    description="Backend API for VeriFi - a RAG-based financial policy chatbot.",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's natural language question.")

    class Config:
        json_schema_extra = {
            "example": {"query": "What is the company's remote work policy?"}
        }


class Source(BaseModel):
    doc: str = Field(..., description="Name/title of the source document.")
    page: int = Field(..., description="Page number the snippet was pulled from.")
    snippet: str = Field(..., description="Short excerpt supporting the answer.")
    score: float = Field(..., description="Relevance score, 0.0-1.0.")


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Found 3 relevant passages for your query.",
                "sources": [
                    {
                        "doc": "terms-and-conditions.pdf",
                        "page": 12,
                        "snippet": "If a margin call is issued, the client must deposit funds within 3 days.",
                        "score": 0.94,
                    }
                ],
            }
        }


class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    chunks_ok, _cli_ok = _check_retrieval_ready()
    if chunks_ok:
        return {"status": "ok"}
    return {"status": "degraded"}


def _run_search(embedding: list[float], top_k: int = 5) -> list[dict]:
    if _use_cpp_cli:
        return vector_client.search(embedding, top_k=top_k)
    return fallback_search.search(embedding, top_k=top_k)


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest):
    if not _retrieval_ready:
        return {
            "answer": (
                f"Vector retrieval is unavailable: chunks file missing at "
                f"{CHUNKS_PATH}. Ask the ingestion team to generate "
                "output/chunks.jsonl."
            ),
            "sources": [],
        }

    try:
        embedding = embedder.embed_query(request.query)
        raw_results = _run_search(embedding, top_k=5)
        sources = mapper.to_sources(raw_results)
    except Exception as exc:
        logger.exception("Retrieval failed")
        return {
            "answer": f"Retrieval failed: {exc}",
            "sources": [],
        }

    count = len(sources)
    if count == 0:
        return {
            "answer": (
                f"No relevant passages found for: \"{request.query}\". "
                "The vector store may still be loading or Chris's search "
                "implementation may need to be completed."
            ),
            "sources": [],
        }

    engine = "C++ VectorStore" if _use_cpp_cli else "Python fallback (pending C++ CLI)"
    return {
        "answer": (
            f"Found {count} relevant passage{'s' if count != 1 else ''} "
            f"for your query. [{engine}] "
            "LLM answer generation will be added in a later story."
        ),
        "sources": sources,
    }
