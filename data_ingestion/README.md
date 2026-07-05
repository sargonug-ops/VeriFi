# Data Ingestion

Data ingestion is Role 1 of VeriFi. It turns verified Fidelity PDFs into chunk records that Role 2 can load into the vector store.

Current pipeline:

```text
PDF files -> page text -> word-safe chunks -> embeddings -> JSONL
```

Generated handoff file:

```text
output/chunks.jsonl
```

## Quick Start

Run these commands from the repo root:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python data_ingestion/main.py
```

If `.venv` does not exist yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data_ingestion/main.py
```

Expected output for the current sample PDF set:

```text
Documents: 2
Pages: 6
Chunks: 35
Output written to: output/chunks.jsonl
```

The first run may take longer because Sentence Transformers downloads the embedding model.

## Input Documents

Put verified Fidelity PDFs directly in:

```text
source_files/
```

The pipeline automatically processes every `.pdf` file directly inside `source_files/`. Files are processed in sorted filename order so output is deterministic.

Current source files:

```text
source_files/privacy.pdf
source_files/terms-and-conditions.pdf
```

## What Role 2 Should Use

Role 2 should read:

```text
output/chunks.jsonl
```

This is a JSONL file, not a normal JSON array. Each line is one independent JSON object.

Correct loading approach:

1. Open `output/chunks.jsonl`.
2. Read one line at a time.
3. Parse that line as JSON.
4. Store the parsed chunk in the vector database.
5. Use `embedding` for similarity search.
6. Keep `text`, `source_document`, and `page_number` for answer context and citations.

Do not parse the entire file as one JSON object.

## Output Schema

Each line has this shape:

```json
{
  "chunk_index": 0,
  "text": "1 TERMS AND CONDITIONS For purposes of these Terms and Conditions...",
  "source_document": "terms-and-conditions.pdf",
  "page_number": 1,
  "embedding": [0.0267649535, -0.0358008891, -0.072021015]
}
```

Field contract:

| Field | Type | Meaning |
| --- | --- | --- |
| `chunk_index` | integer | Zero-based chunk ID in the combined output file |
| `text` | string | Human-readable chunk text to use in RAG context |
| `source_document` | string | Original PDF filename |
| `page_number` | integer | One-based page number from the source PDF |
| `embedding` | array of numbers | Vector representation of `text` |

Current embedding details:

| Property | Value |
| --- | --- |
| Model | `all-MiniLM-L6-v2` |
| Library | `sentence-transformers` |
| Vector length | `384` |

## Suggested Role 2 Data Shape

For the C++ vector-store role, the record maps naturally to a struct like:

```cpp
struct DocumentChunk {
    int chunk_index;
    std::string text;
    std::string source_document;
    int page_number;
    std::vector<float> embedding;
};
```

For retrieval, search over `embedding`. After finding matching chunks, return `text` plus citation metadata:

```text
source_document, page_number
```

Example citation display:

```text
terms-and-conditions.pdf, page 1
```

## Validate The JSONL

Use this from the repo root after running ingestion:

```bash
.venv/bin/python - <<'PY'
import json
from collections import Counter, defaultdict
from pathlib import Path

path = Path("output/chunks.jsonl")
records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
required = {"chunk_index", "text", "source_document", "page_number", "embedding"}
pages_by_document = defaultdict(Counter)

for record in records:
    pages_by_document[record["source_document"]][record["page_number"]] += 1

print("records:", len(records))
print("missing required fields:", sum(1 for record in records if not required <= record.keys()))
print("empty text chunks:", sum(1 for record in records if not record["text"]))
print("contiguous chunk indexes:", [record["chunk_index"] for record in records] == list(range(len(records))))
print("documents:", dict(sorted(Counter(record["source_document"] for record in records).items())))
print("pages by document:", {doc: dict(sorted(pages.items())) for doc, pages in sorted(pages_by_document.items())})
print("embedding lengths:", dict(sorted(Counter(len(record["embedding"]) for record in records).items())))
print("all embedding values numeric:", all(isinstance(value, (int, float)) for record in records for value in record["embedding"]))
PY
```

Expected current validation:

```text
records: 35
missing required fields: 0
empty text chunks: 0
contiguous chunk indexes: True
documents: {'privacy.pdf': 18, 'terms-and-conditions.pdf': 17}
pages by document: {'privacy.pdf': {1: 8, 2: 5, 3: 5}, 'terms-and-conditions.pdf': {1: 6, 2: 7, 3: 4}}
embedding lengths: {384: 35}
all embedding values numeric: True
```

## File Overview

| File | Purpose |
| --- | --- |
| `main.py` | Finds PDFs in `source_files/` and runs the complete ingestion pipeline |
| `pdf_reader.py` | Extracts text from PDFs page-by-page using PyMuPDF |
| `chunker.py` | Cleans text and creates chunks without splitting words |
| `embedder.py` | Adds `embedding` arrays using Sentence Transformers |
| `jsonl_writer.py` | Writes records to `output/chunks.jsonl` |

## Format Stability

The existing fields should be treated as stable:

```text
chunk_index
text
source_document
page_number
embedding
```

Future changes should add new fields instead of renaming or removing these fields. This lets Role 2 keep the same parser and `DocumentChunk` structure.

## Known Limits

- The pipeline processes `.pdf` files directly inside `source_files/`; it does not recursively scan nested folders.
- Chunking is word-safe and keeps chunks around `1000` characters, but it is not semantic section chunking yet.
- Embeddings are generated locally with Sentence Transformers, not through an external API.
- The generated `output/chunks.jsonl` file can be recreated at any time by rerunning `python data_ingestion/main.py`.
