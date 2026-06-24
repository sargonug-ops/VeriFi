# Backend Bridge — Dev Setup

## What's in here

```
backend-bridge/
├── CMakeLists.txt        # fetches cpp-httplib, nlohmann/json, cpr automatically
├── src/
│   └── main.cpp           # GET /health, POST /chat (mock data), CORS, error handling
├── system_prompt.txt       # placeholder — loaded at runtime, not hardcoded (Sprint 2+)
├── .env.example            # template for secrets — copy to .env, never commit .env
└── .gitignore
```

# Purpose

The API/Backend Bridge establishes an HTTP server that handles requests from the frontend and delivers grounded, citable results back to it.

The server accepts a user's message as a query, converts it to a vector embedding, sends that vector to the vector database, and receives the top-K most relevant document chunks. Those chunks are formatted as context for the LLM, which generates a grounded answer. The same chunks' metadata (document name, page, snippet, score) are also returned separately as a `sources` array, so the frontend can display citations alongside the generated answer.

This is the connective layer between three independently-built components — the vector database, the external LLM API, and the React frontend — and is responsible for defining the JSON contract each of them builds against.




