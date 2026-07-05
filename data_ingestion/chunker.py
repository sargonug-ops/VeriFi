def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x07", " ")
    text = " ".join(text.split())
    return text


def get_overlap_start(words, chunk_start, chunk_end, overlap):
    if overlap <= 0:
        return chunk_end

    overlap_start = chunk_end
    overlap_chars = 0

    while overlap_start > chunk_start:
        word = words[overlap_start - 1]
        added_chars = len(word)

        if overlap_chars > 0:
            added_chars += 1

        if overlap_chars + added_chars > overlap:
            break

        overlap_start -= 1
        overlap_chars += added_chars

    if overlap_start == chunk_start:
        return chunk_end

    return overlap_start


def chunk_text(text, max_chars=1000, overlap=100):
    if not text:
        return []

    text = clean_text(text)
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start
        current_length = 0

        while end < len(words):
            word = words[end]
            added_length = len(word) if current_length == 0 else len(word) + 1

            if current_length > 0 and current_length + added_length > max_chars:
                break

            current_length += added_length
            end += 1

        chunk = " ".join(words[start:end])
        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = get_overlap_start(words, start, end, overlap)

    return chunks


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
