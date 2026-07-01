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

```text
output/chunks.jsonl
```

Example record:

```json
{
    "chunk_index": 0,
    "text": "...",
    "source_document": "terms-and-conditions.pdf",
    "page_number": 1
}
```

One JSON object per line.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python data_ingestion/main.py
```

Expected output:

```text
Pages: 3
Chunks: 18
Output written to: output/chunks.jsonl
```

## Current Status

Implemented:
- PDF text extraction
- Text chunking
- JSONL export

Planned:
- Embedding generation
- Improved chunking strategy
- Multi-document ingestion