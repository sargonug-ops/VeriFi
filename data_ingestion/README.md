# Data Ingestion

Reads Fidelity PDFs from `source_files/`, extracts text page-by-page, splits it
into readable chunks, generates an embedding for each chunk, and writes records
to `output/chunks.jsonl` for the C++ vector store.

## Vector store handoff

Use this file as the vector database input:

Do not parse the entire file as one JSON object.

Each line is one complete JSON object. Read the file line-by-line, parse each
line as JSON, and load each record into the vector store.

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

For the current model (`all-MiniLM-L6-v2`), embeddings have length `384`.

## How to regenerate

## Suggested Role 2 Data Shape

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data_ingestion/main.py
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

The first run may take longer because `sentence-transformers` downloads the
embedding model.

## Format Stability

```text
chunk_index
text
source_document
page_number
embedding
```

The pipeline is configured for this PDF in `data_ingestion/main.py`.

## Implementation files

- `main.py`: runs the full pipeline
- `pdf_reader.py`: extracts page text from PDFs using PyMuPDF
- `chunker.py`: creates readable chunks without splitting words
- `embedder.py`: generates embeddings using Sentence Transformers
- `jsonl_writer.py`: writes one JSON object per line to JSONL

## Notes for the vector store

- Do not treat the whole JSONL file as one JSON array.
- Preserve `source_document` and `page_number` so chatbot answers can cite sources.
- Use `text` as the human-readable context and `embedding` as the search input.
- The output format is intended to stay stable; prefer adding fields over renaming
  or removing existing ones.
