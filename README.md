# VeriFi

A C++ and React RAG chatbot that grounds answers in verified policy documents.

**Live demo (GitHub Pages):** [https://kurisuo.github.io/VeriFi/](https://kurisuo.github.io/VeriFi/)

## Problem Statement

Chatbots deployed across company websites often confidently hallucinate information when handling dense policy inquiries that typically require a human agent. This creates a massive regulatory and financial liability for businesses.

Traditional search tools fail to solve this issue because they rely primarily on exact keyword matches, completely missing the true semantic meaning behind a consumer's question. Our application solves this by forcing the AI to base its conversational responses strictly on real, verified company policy documents retrieved dynamically at query time.

## How It Works

We designed VeriFi to run in two phases — one that happens once, ahead of
time, and one that runs on every question.

**Setup (once):** The policy documents are split into small passages
("chunks"), and an embedding model converts each chunk into a vector — a list
of numbers that captures its meaning. Every chunk and its vector are loaded
into the in-memory C++ vector store.

**Per query (every question):**
1. A user asks a question in the React interface.
2. The same embedding model converts that question into a vector.
3. The C++ vector store compares the question vector against every stored
   chunk using cosine similarity and returns the top-K most semantically
   relevant passages.
4. Those passages, the question, and a grounding system prompt are assembled
   into a single request to the LLM.
5. The LLM produces a conversational answer constrained to the retrieved
   passages, and the UI displays it with citations to the source documents.

Because the LLM only ever sees passages actually retrieved from verified
documents, its answers stay anchored to real sources — which reduces
hallucination, though it does not eliminate it.

## Project Goals

1. **Custom vector database:** Implement a fast semantic vector store from scratch (a lightweight Pinecone-style engine) that locates documents by geometric meaning rather than keyword matching.

2. **End-to-end RAG pipeline:** Integrate the C++ search engine into a full-stack Retrieval-Augmented Generation flow that reduces hallucinations by grounding responses in verified facts.

3. **Focused scope:** Restrict the dataset to official policy documents available from Fidelity Investments so the project stays demoable within the development cycle.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Vite, React Router, TanStack Query |
| Backend API | FastAPI (`GET /health`, `POST /chat`) |
| Vector store | C++17 in-memory cosine k-NN (`VectorStore`) |
| Ingestion | Python, PyMuPDF, Sentence Transformers (`all-MiniLM-L6-v2`, 384-dim) |
| Hosting | GitHub Pages (static frontend + MSW mocks) |

## Repository layout

```text
frontend/          React chat UI (landing + chat, citations, MSW mocks)
backend/           FastAPI bridge + C++ VectorStore (headers, src, tests)
data_ingestion/    PDF → chunks → embeddings → output/chunks.jsonl
source_files/      Source policy PDFs
.github/workflows/ Deploy frontend to GitHub Pages on every push to main
```

## Quick start

### Frontend (local)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: `http://localhost:5173`

By default `VITE_USE_MOCKS=true`, so the UI works without a running backend.
See [`frontend/README.md`](frontend/README.md) for connecting to FastAPI.

### Backend API (local)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn --app-dir src main:app --reload --port 8000
```

Health check: `http://localhost:8000/health`  
Swagger: `http://localhost:8000/docs`

Full backend + C++ vector-store setup: [`backend/SETUP.md`](backend/SETUP.md)

### Data ingestion (regenerate chunks)

From the repo root:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python data_ingestion/main.py
```

Details: [`data_ingestion/README.md`](data_ingestion/README.md)

## GitHub Pages deployment

Every push to `main` builds the **current** `frontend/` tree and publishes it to
GitHub Pages via [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

| Setting | Value |
|---------|--------|
| Live URL | https://kurisuo.github.io/VeriFi/ |
| Trigger | Push to `main`, or manual **workflow_dispatch** |
| Build | `npm ci && npm run build` in `frontend/` |
| Base path | `/VeriFi/` (`GITHUB_PAGES=true`) |
| API mode | `VITE_USE_MOCKS=true` (static host; no FastAPI on Pages) |

What this means in practice:

- Merging frontend changes to `main` is enough — the workflow rebuilds from
  source, so Pages always reflects the latest committed UI (not a checked-in
  `dist/` folder).
- The Pages site uses MSW mock chat responses. For a live FastAPI / C++ RAG
  stack, run the apps locally as above.
- SPA routes (`/chat`) work on Pages because the build copies `index.html` to
  `404.html`.

To redeploy without a code change: GitHub → **Actions** → **Deploy frontend to
GitHub Pages** → **Run workflow**.

## Team roles

1. **Data Ingestion** [Srushti]: Sources public PDFs, chunks text, generates embeddings into `chunks.jsonl`.

2. **Vector Store / Project Owner** [ChristopherZarraga]: C++ memory structures, cosine similarity, O(N) ranking, load/search APIs.

3. **API / Backend Bridge** [Ethan]: FastAPI server, JSON contract, CORS, wiring to embedding/LLM services.

4. **Frontend** : React chat dashboard, landing → chat handoff, loading states, source citations.

5. **Integration, Prompting & QA** : Grounding prompts, edge-case testing, GitHub/Pages release readiness, live demo.
