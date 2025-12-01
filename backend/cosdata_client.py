
# CosData-only client for Sahayak
import os
from cosdata import Client

COSDATA_HOST = os.getenv("COSDATA_HOST", "http://127.0.0.1:8443")
COSDATA_USER = os.getenv("COSDATA_USER", "admin")
COSDATA_PASS = os.getenv("COSDATA_PASS", "admin")

client = Client(
    host=COSDATA_HOST,
    username=COSDATA_USER,
    password=COSDATA_PASS,
    verify=False
)

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
