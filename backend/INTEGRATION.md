# VectorStore Integration Contract (for Chris)

Ethan's API bridge calls Chris's `VectorStore` through `search_cli` — a thin
adapter in `backend/src/search_cli.cpp`. The bridge does **not** modify
`VectorStore.cpp`, `VectorStore.h`, or `DocumentChunk.h`.

## Required public API

```cpp
VectorStore store;
store.load_from_jsonl("output/chunks.jsonl");  // must return true on success
auto results = store.search(query_embedding, top_k);
```

Each `SearchResult` must contain:

| Field | Type |
|-------|------|
| `score` | `float` — cosine similarity |
| `text` | `std::string` |
| `source_document` | `std::string` |
| `page_number` | `int` |

## Input data

`output/chunks.jsonl` — one JSON object per line:

```json
{
  "chunk_index": 0,
  "text": "...",
  "source_document": "terms-and-conditions.pdf",
  "page_number": 1,
  "embedding": [384 floats]
}
```

Embeddings must be 384-dimensional (`all-MiniLM-L6-v2`).

## Build (once VectorStore compiles)

From `backend/`:

```bash
g++ -std=c++17 -Iinclude -Ilib src/VectorStore.cpp src/search_cli.cpp -o search_cli
```

Or use the VS Code task **Build search_cli**.

## Current blockers (Chris's side)

- `load_from_jsonl()` returns `false` (stub)
- `search()` has compile errors and returns `{}`

Once these are fixed, the FastAPI bridge will return real `sources[]` automatically.
