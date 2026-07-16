"""Path and runtime configuration for the retrieval bridge."""

from pathlib import Path

# backend/retrieval/config.py -> backend/ -> repo root
BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_DIR.parent

SEARCH_CLI_PATH = Path(
    __import__("os").environ.get("SEARCH_CLI_PATH", BACKEND_DIR / "search_cli")
)
CHUNKS_PATH = Path(
    __import__("os").environ.get("CHUNKS_PATH", REPO_ROOT / "output" / "chunks.jsonl")
)
TOP_K = int(__import__("os").environ.get("TOP_K", "5"))
EMBEDDING_MODEL = __import__("os").environ.get(
    "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
)
SEARCH_TIMEOUT_SECONDS = float(
    __import__("os").environ.get("SEARCH_TIMEOUT_SECONDS", "30")
)
