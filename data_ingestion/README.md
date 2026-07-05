## current chunking cuts off words and is not semantic

## For Role 2 (Vector Store)

The generated `output/chunks.jsonl` file is ready to load directly into the vector store. Each line contains one chunk of text along with its source document and page number. Right now there are no embeddings, so you'll need to either generate embeddings yourself or wait for the next ingestion update. For testing, you can load each JSON object into a `DocumentChunk` structure and verify parsing, metadata handling, indexing, and retrieval logic. The file format should remain stable, with future updates only adding fields (such as `embedding`) rather than changing existing ones.


# Data Ingestion

Reads Fidelity PDFs, extracts text, chunks it, and exports the chunks to a JSONL file for the vector store.

## Files

### main.py
Runs the entire pipeline.

### pdf_reader.py
Reads a PDF and extracts text page-by-page.

### chunker.py
Splits extracted text into smaller chunks while keeping page metadata.

### jsonl_writer.py
Writes chunk records to `output/chunks.jsonl`.

## Input

Place PDFs in:

```text
source_files/
```

Current example:

```text
source_files/terms-and-conditions.pdf
```

## Output

Generated file:
=======
# Data Ingestion

This folder generates the JSONL input used by the vector store role.

The pipeline reads Fidelity PDFs from `source_files/`, extracts text page-by-page, splits the text into readable chunks, generates an embedding for each chunk, and writes the final records to `output/chunks.jsonl`.

## Vector Store Handoff

Use this file as the vector database input:
>>>>>>> theirs

```text
output/chunks.jsonl
```

Each line is one complete JSON object. Read the file line-by-line, parse each line as JSON, and load each record into the vector store.

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

For the current model, embeddings have length `384`.

## How To Regenerate The File

Run all commands from the repo root.

Create a virtual environment if one does not already exist:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ingestion pipeline:

```bash
python data_ingestion/main.py
```

Expected output for the current sample PDF:

```text
Pages: 3
Chunks: 17
Output written to: output/chunks.jsonl
```

The first run may take longer because `sentence-transformers` downloads the embedding model.

## Input PDF

Current input:

```text
source_files/terms-and-conditions.pdf
```

The current pipeline is configured for this PDF in `data_ingestion/main.py`.

## Implementation Files

- `main.py`: runs the full pipeline
- `pdf_reader.py`: extracts page text from PDFs using PyMuPDF
- `chunker.py`: creates readable chunks without splitting words
- `embedder.py`: generates embeddings using Sentence Transformers
- `jsonl_writer.py`: writes one JSON object per line to JSONL

## Notes For Role 2

- Do not treat the whole JSONL file as one JSON array.
- Preserve `source_document` and `page_number` so chatbot answers can cite where the information came from.
- Use `text` as the human-readable context and `embedding` as the vector search input.
- The output format is intended to stay stable. Future changes should add fields rather than rename or remove the existing fields.
