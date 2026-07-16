"""Call Chris's VectorStore via the search_cli subprocess adapter."""

import json
import logging
import subprocess
from typing import Any

from .config import CHUNKS_PATH, SEARCH_CLI_PATH, SEARCH_TIMEOUT_SECONDS, TOP_K

logger = logging.getLogger(__name__)


class VectorSearchError(Exception):
    """Raised when the C++ vector search CLI fails."""


def is_cli_available() -> bool:
    return SEARCH_CLI_PATH.is_file() and CHUNKS_PATH.is_file()


def search(embedding: list[float], top_k: int | None = None) -> list[dict[str, Any]]:
    if top_k is None:
        top_k = TOP_K

    if not SEARCH_CLI_PATH.is_file():
        raise VectorSearchError(
            f"search_cli binary not found at {SEARCH_CLI_PATH}. "
            "Build it with the VS Code task 'Build search_cli' once VectorStore compiles."
        )

    if not CHUNKS_PATH.is_file():
        raise VectorSearchError(f"chunks file not found at {CHUNKS_PATH}")

    payload = json.dumps({"embedding": embedding, "top_k": top_k})

    try:
        completed = subprocess.run(
            [str(SEARCH_CLI_PATH), str(CHUNKS_PATH)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=SEARCH_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise VectorSearchError("search_cli timed out") from exc
    except OSError as exc:
        raise VectorSearchError(f"failed to run search_cli: {exc}") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown error"
        raise VectorSearchError(
            f"search_cli exited with code {completed.returncode}: {stderr}"
        )

    stdout = completed.stdout.strip()
    if not stdout:
        return []

    try:
        results = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise VectorSearchError(f"search_cli returned invalid JSON: {exc}") from exc

    if not isinstance(results, list):
        raise VectorSearchError("search_cli response must be a JSON array")

    return results
