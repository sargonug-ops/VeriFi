# Backend Bridge — Dev Setup

# Purpose

The API/Backend Bridge establishes an HTTP server that handles requests from the frontend and delivers grounded, citable results back to it.

The server accepts a user's message as a query, converts it to a vector embedding, sends that vector to the vector database, and receives the top-K most relevant document chunks. Those chunks are formatted as context for the LLM, which generates a grounded answer. The same chunks' metadata (document name, page, snippet, score) are also returned separately as a `sources` array, so the frontend can display citations alongside the generated answer.

This is the connective layer between three independently-built components — the vector database, the external LLM API, and the React frontend — and is responsible for defining the JSON contract each of them builds against.

# VeriFi Backend

FastAPI server for User Story 1.4 — a running `/chat` endpoint with a
defined contract so the frontend can build against mocked data.

## Requirements

- Python 3.10+ (works on 3.10–3.12; confirm with `python3 --version`)
- pip

## Setup (same steps on Mac / Linux / Windows)

```bash
# 1. Clone the repo, then cd into the backend folder
cd verifi-backend

# 2. Create a virtual environment
python3 -m venv venv          # Windows: python -m venv venv

# 3. Activate it
source venv/bin/activate      # Windows (cmd):        venv\Scripts\activate.bat
                               # Windows (PowerShell): venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Verify it works

```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the remote work policy?"}'
```

Or just open `http://localhost:8000/docs` in a browser for interactive
Swagger docs — you can call both endpoints from there without curl.

## What's in scope for this story (1.4)

- `GET /health` → `{"status": "ok"}`
- `POST /chat` → hardcoded mock `{answer, sources}` — **no real RAG
  pipeline wired in yet**, that's a later story.
- CORS configured for `http://localhost:3000` (React dev server).

See `API_CONTRACT.md` for the full request/response schema to build
against.