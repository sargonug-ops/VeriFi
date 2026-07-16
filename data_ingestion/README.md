# Data Ingestion

Reads Fidelity PDFs from `source_files/`, extracts text page-by-page, splits it
into readable chunks, generates an embedding for each chunk, and writes records
to `output/chunks.jsonl` for the C++ vector store.

## Vector store handoff

Use this file as the vector database input:

```text
output/chunks.jsonl
```

Each line is one complete JSON object. Read the file line-by-line, parse each
line as JSON, and load each record into the vector store.

Current output schema:

```json
{
  "chunk_index": 0,
  "text": "...",
  "source_document": "terms-and-conditions.pdf",
  "page_number": 1,
  "embedding": [0.0267, -0.0358, -0.072]
}
```

Fields:

- `chunk_index`: zero-based chunk ID within the generated output file
- `text`: chunk text to display or pass into RAG context
- `source_document`: original PDF filename
- `page_number`: one-based PDF page number for citation/debugging
- `embedding`: numeric vector for semantic search

For the current model (`all-MiniLM-L6-v2`), embeddings have length `384`.

## How to regenerate

Run all commands from the repo root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data_ingestion/main.py
```

Expected output for the current sample PDF:

```text
Pages: 3
Chunks: 17
Output written to: output/chunks.jsonl
```

The first run may take longer because `sentence-transformers` downloads the
embedding model.

## Input PDF

```text
source_files/terms-and-conditions.pdf
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
