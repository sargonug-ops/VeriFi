from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32


def load_model(model_name=MODEL_NAME):
    try:
        return SentenceTransformer(model_name, local_files_only=True)
    except Exception:
        return SentenceTransformer(model_name)


def add_embeddings(records, model_name=MODEL_NAME, batch_size=BATCH_SIZE):
    if not records:
        return []

    model = load_model(model_name)
    texts = [record["text"] for record in records]
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    embedded_records = []

    for record, embedding in zip(records, embeddings):
        embedded_record = record.copy()
        embedded_record["embedding"] = embedding.tolist()
        embedded_records.append(embedded_record)

    return embedded_records
