from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def add_embeddings(records, model_name=MODEL_NAME):
    if not records:
        return []

    model = SentenceTransformer(model_name)
    texts = [record["text"] for record in records]
    embeddings = model.encode(texts, convert_to_numpy=True)

    embedded_records = []

    for record, embedding in zip(records, embeddings):
        embedded_record = record.copy()
        embedded_record["embedding"] = embedding.tolist()
        embedded_records.append(embedded_record)

    return embedded_records
