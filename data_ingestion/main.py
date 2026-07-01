"""
test commit 2
"""
# from pdf_reader import extract_pdf_text


# PDF_PATH = "source_files/terms-and-conditions.pdf"


# def main():
#     pages = extract_pdf_text(PDF_PATH)

#     print(f"\nSuccessfully extracted {len(pages)} pages.\n")

#     for page in pages:
#         print("=" * 80)
#         print(f"PAGE {page['page_number']}")
#         print("=" * 80)

#         text_preview = page["text"][:500]

#         print(text_preview)

#         if len(page["text"]) > 500:
#             print("\n[TRUNCATED]\n")

#         print()
        
#         # for page in pages:
#         #     print(
#         #         f"Page {page['page_number']} length: "
#         #         f"{len(page['text'])} characters"
#         #     )


# if __name__ == "__main__":
#     main()

"""
test commit 3
"""
# from pdf_reader import extract_pdf_text
# from chunker import chunk_pages

# PDF_PATH = "source_files/terms-and-conditions.pdf"


# def main():
#     pages = extract_pdf_text(PDF_PATH)

#     chunks = chunk_pages(
#         pages,
#         source_document="terms-and-conditions.pdf"
#     )

#     print(f"Pages: {len(pages)}")
#     print(f"Chunks: {len(chunks)}")

#     print("\nFIRST CHUNK\n")
#     print(chunks[0])

#     print("\nLAST CHUNK\n")
#     print(chunks[-1])


# if __name__ == "__main__":
#     main()   

"""
test commit 4
"""

from pdf_reader import extract_pdf_text
from chunker import chunk_pages
from jsonl_writer import write_jsonl

PDF_PATH = "source_files/terms-and-conditions.pdf"
OUTPUT_PATH = "output/chunks.jsonl"


def main():
    pages = extract_pdf_text(PDF_PATH)

    chunks = chunk_pages(
        pages,
        source_document="terms-and-conditions.pdf"
    )

    write_jsonl(chunks, OUTPUT_PATH)

    print(f"Pages: {len(pages)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Output written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()