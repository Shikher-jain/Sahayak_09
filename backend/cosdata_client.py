
# CosData-only client for Sahayak
import os
from cosdata import Client

COSDATA_HOST = os.getenv("COSDATA_HOST", "http://127.0.0.1:8443")
COSDATA_USER = os.getenv("COSDATA_USER", "admin")
COSDATA_PASS = os.getenv("COSDATA_PASS", "admin")


# Fallback local storage
_local_db = []

_client = None

def get_client():
    """Lazy initialization of CosData client"""
    global _client
    if _client is None:
        try:
            _client = Client(
                host=COSDATA_HOST,
                username=COSDATA_USER,
                password=COSDATA_PASS,
                verify=False
            )
        except Exception as e:
            print("CosData Cloud unavailable, using local fallback.", e)
            _client = None
    return _client

def insert_vector(text, metadata):
    client = get_client()
    if client:
        try:
            vector = client.embeddings.create(text=text)
            doc = client.documents.create(
                content=text,
                metadata=metadata,
                embedding=vector.embedding
            )
            return doc.id
        except Exception as e:
            print("CosData Cloud error, using local fallback.", e)
    # Fallback: store locally
    doc_id = f"local_{len(_local_db)+1}"
    _local_db.append({"id": doc_id, "content": text, "metadata": metadata})
    return doc_id

def search(query):
    client = get_client()
    if client:
        try:
            vector = client.embeddings.create(text=query)
            results = client.search.query(
                embedding=vector.embedding,
                top_k=5
            )
            return results
        except Exception as e:
            print("CosData Cloud error, using local fallback.", e)
    # Fallback: naive local search
    results = []
    for doc in _local_db:
        if query.lower() in doc["content"].lower():
            results.append(doc)
    return results[:5]

# Example usage:
if __name__ == "__main__":
    # Index a document
    metadata = {"source": "pdf", "title": "Sample PDF"}
    doc_id = insert_vector("This is the content of the PDF.", metadata)
    print("Document indexed with ID:", doc_id)

    # Perform a semantic search
    results = search("What is the summary of the document?")
    for item in results:
        print("Text:", item.get("content", ""))
        print("Metadata:", item.get("metadata", {}))