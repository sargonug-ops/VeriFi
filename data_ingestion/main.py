from pathlib import Path

from chunker import chunk_pages
from embedder import add_embeddings
from jsonl_writer import write_jsonl
from pdf_reader import extract_pdf_text


SOURCE_DIR = Path("source_files")
OUTPUT_PATH = Path("output/chunks.jsonl")


def find_pdf_files(source_dir=SOURCE_DIR):
    return sorted(source_dir.glob("*.pdf"))


def build_chunk_records(pdf_files):
    all_chunks = []
    total_pages = 0

    for pdf_path in pdf_files:
        pages = extract_pdf_text(str(pdf_path))
        total_pages += len(pages)

        chunks = chunk_pages(
            pages,
            source_document=pdf_path.name
        )

        all_chunks.extend(chunks)

    for chunk_index, chunk in enumerate(all_chunks):
        chunk["chunk_index"] = chunk_index

    return all_chunks, total_pages


def main():
    pdf_files = find_pdf_files()

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {SOURCE_DIR}")

    chunks, total_pages = build_chunk_records(pdf_files)
    chunks = add_embeddings(chunks)

    write_jsonl(chunks, str(OUTPUT_PATH))

    print(f"Documents: {len(pdf_files)}")
    print(f"Pages: {total_pages}")
    print(f"Chunks: {len(chunks)}")
    print(f"Output written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
