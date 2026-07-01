
#text: full page
#max_chars: max chars per chunk
#overlap: repeated chars
def chunk_text(text, max_chars=1000, overlap=100):
   
    if not text:
        return []

    # text = " ".join(text.split())
    text = text.replace("\x07", " ")
    text = " ".join(text.split())   

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

    return chunks


#pages: output from from extract_pdf_text() in main
def chunk_pages(pages, source_document, max_chars=1000, overlap=100):

    records = []
    chunk_index = 0

    for page in pages:
        page_chunks = chunk_text(
            page["text"],
            max_chars=max_chars,
            overlap=overlap
        )

        for chunk in page_chunks:
            records.append({
                "chunk_index": chunk_index,
                "text": chunk,
                "source_document": source_document,
                "page_number": page["page_number"]
            })

            chunk_index += 1

    return records