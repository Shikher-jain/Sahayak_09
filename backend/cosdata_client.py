
# CosData-only client for Sahayak
import os
from cosdata import CosDataClient

COSDATA_API_KEY = os.getenv("COSDATA_API_KEY")
COSDATA_HOST = os.getenv("COSDATA_HOST", "https://api.cosdata.io")

client = CosDataClient(api_key=COSDATA_API_KEY, host=COSDATA_HOST)

def insert_vector(text, metadata):
    vector = client.embeddings.create(text=text)
    doc = client.documents.create(
        content=text,
        metadata=metadata,
        embedding=vector.embedding
    )
    return doc.id

def search(query):
    vector = client.embeddings.create(text=query)
    results = client.search.query(
        embedding=vector.embedding,
        top_k=5
    )
    return results
