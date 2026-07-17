# Backend setup — FastAPI bridge + C++ vector store

## Purpose

The backend is the connective layer between three components: the C++ vector
database, external embedding/LLM APIs, and the React frontend.

Today the HTTP surface is a FastAPI server that exposes a stable JSON contract
(`GET /health`, `POST /chat`) the frontend builds against. The C++
`VectorStore` loads ingestion’s `chunks.jsonl`, ranks passages by cosine
similarity, and is exercised via unit/benchmark binaries. Wiring search into
`/chat` for a live RAG path is the remaining integration step.

## Requirements

### FastAPI (HTTP API)

- Python 3.10+ (`python3 --version`)
- pip

### C++ vector store (build & tests)

- C++17 compiler (`clang++` or `g++`)
- No external C++ package manager required — JSON parsing uses the vendored
  header at `backend/lib/json.hpp`

### Shared data

- Ingestion output at repo-root `output/chunks.jsonl` (or a path you pass in),
  with 384-dimensional embeddings from `all-MiniLM-L6-v2`

## FastAPI setup (Mac / Linux / Windows)

```bash
# 1. From the repo root, enter the backend folder
cd backend

# 2. Create a virtual environment
python3 -m venv venv          # Windows: python -m venv venv

# 3. Activate it
source venv/bin/activate      # Windows (cmd):        venv\Scripts\activate.bat
                               # Windows (PowerShell): venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server (main.py lives under src/)
uvicorn --app-dir src main:app --reload --port 8000
```

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Verify the API

```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the remote work policy?"}'
```

Or open `http://localhost:8000/docs` for interactive Swagger UI.

### CORS & frontend

- Dev UI runs on Vite at `http://localhost:5173`.
- Preferred local setup: keep `VITE_API_URL=/api` and
  `VITE_USE_MOCKS=false` in `frontend/.env`. Vite proxies `/api/*` to
  `localhost:8000`, so you do not need CORS changes for day-to-day work.
- The FastAPI app currently allows `http://localhost:3000` in CORS middleware;
  if you call the API directly from the browser (no proxy), add
  `http://localhost:5173` to `allow_origins` in `src/main.py`.

## API contract

### `GET /health`

```json
{ "status": "ok" }
```

### `POST /chat`

Request:

```json
{ "query": "What happens if a margin call is issued?" }
```

Response:

```json
{
  "answer": "...",
  "sources": [
    {
      "doc": "terms-and-conditions.pdf",
      "page": 12,
      "snippet": "...",
      "score": 0.94
    }
  ]
}
```

Field names on the wire are `doc`, `page`, `snippet`, and `score`. The React
app normalizes these to UI types in `frontend/src/api/normalize.ts`.

**Current `/chat` behavior:** returns a stable mocked `{ answer, sources }`
payload so the frontend can ship and demo without the full RAG stack. Real
retrieval will call `VectorStore::search()` and an LLM once that bridge is
connected.

## C++ VectorStore

### Layout

```text
backend/
├── include/
│   ├── DocumentChunk.h   # chunk + SearchResult structs (matches JSONL)
│   └── VectorStore.h     # load_from_jsonl, search, fetchSize, dimension
├── src/
│   ├── VectorStore.cpp   # cosine k-NN implementation
│   └── main.py           # FastAPI app
├── lib/
│   └── json.hpp          # nlohmann/json (header-only)
└── tests/
    ├── test_vectorstore.cpp
    └── bench_vectorstore.cpp
```

Expected embedding dimension: **384**. Chunks whose embedding length differs
are skipped during `load_from_jsonl`.

### Build & run the test harness

From `backend/`:

```bash
clang++ -std=c++17 -O2 -Iinclude -Ilib \
  src/VectorStore.cpp tests/test_vectorstore.cpp \
  -o test_vectorstore

# Needs output/chunks.jsonl (generate via data_ingestion, or adjust the path
# inside tests/test_vectorstore.cpp)
./test_vectorstore
```

On Windows with MSYS2/MinGW (matches `.vscode/tasks.json`):

```bash
g++ -std=c++17 -Iinclude -Ilib \
  src/VectorStore.cpp tests/test_vectorstore.cpp \
  -o test_vs
```

With the sample Fidelity PDF, a successful load prints roughly
`chunks=17 dim=384`.

### Benchmarks

```bash
clang++ -std=c++17 -O2 -Iinclude -Ilib \
  src/VectorStore.cpp tests/bench_vectorstore.cpp \
  -o bench_vectorstore

./bench_vectorstore [scratch_dir]
```

`scratch_dir` defaults to `/tmp/verifi_bench`. The harness writes synthetic
384-dim JSONL fixtures and measures load + search throughput; it does not
require the real policy corpus.

## Deployed frontend vs local backend

| Environment | What runs |
|-------------|-----------|
| [GitHub Pages](https://kurisuo.github.io/VeriFi/) | Static React build only; `VITE_USE_MOCKS=true` |
| Local full stack | Vite UI + this FastAPI server (+ C++ store when wired) |

Pages is rebuilt from `frontend/` on every push to `main`. Backend Python/C++
code is **not** hosted on Pages — run it locally (or on a separate server)
when you need a real `/chat` backend.

See the root [README](../README.md) for the Pages workflow summary and
[`frontend/README.md`](../frontend/README.md) for UI env vars.
