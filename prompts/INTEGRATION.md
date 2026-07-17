# VeriFi Prompts Integration Handoff

**Author:** Divya Machiraju  
**For:** Ethan (Backend / API)  
**Sprint:** Sprint 3 — User Story 3.4

## What this module does

After vector retrieval returns chunks, call `generate_rag_response()` to:
1. Build the grounded prompt
2. Call the LLM
3. Return `{"answer": str, "sources": [...]}`

## How to wire into `backend/src/main.py`

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "prompts"))

from rag_pipeline import generate_rag_response

# Inside POST /chat, after vector retrieval:
retrieved = [
    {"text": "...", "source_document": "...", "page_number": 1, "score": 0.92},
    # ... from VectorStore search results
]
return generate_rag_response(request.query, retrieved)

```

## Source format

`generate_rag_response` returns sources as:
- `text`
- `source_document`
- `page_number`
- `score`

If the frontend still expects legacy `doc` / `page` / `snippet`, map in the backend before returning.

## Environment variables

- `OPENAI_API_KEY` — required for real LLM
- `VERIFI_USE_MOCK_LLM=true` — for local testing without API
- `VERIFI_LLM_MODEL` — optional, defaults to `gpt-4o-mini`