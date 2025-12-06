# CosData-only client for Sahayak
import os
import logging
from cosdata import Client

# Initialize logger
logger = logging.getLogger("cosdata-client")
logger.setLevel(logging.INFO)

COSDATA_HOST = os.getenv("COSDATA_HOST", "http://127.0.0.1:8443")
COSDATA_USER = os.getenv("COSDATA_USER", "admin")
COSDATA_PASS = os.getenv("COSDATA_PASS", "admin")


# Fallback local storage
_local_db = []

_client = None

def get_client():
    """Lazy initialization of CosData client with detailed logging."""
    global _client
    if _client is None:
        try:
            logger.info("Initializing CosData client...")
            _client = Client(
                host=COSDATA_HOST,
                username=COSDATA_USER,
                password=COSDATA_PASS,
                verify=False
            )
            logger.info("CosData client initialized successfully.")
        except Exception as e:
            logger.error("Failed to initialize CosData client. Using local fallback.", exc_info=True)
            _client = None
    return _client

def validate_metadata(metadata):
    """Validate metadata to ensure required fields are present."""
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary.")
    # Example validation: Ensure 'source' field exists
    if 'source' not in metadata:
        raise ValueError("Metadata must contain a 'source' field.")

def insert_vector(text, metadata):
    try:
        validate_metadata(metadata)
    except ValueError as e:
        logger.error(f"Metadata validation error: {e}")
        raise

    client = get_client()
    if client:
        try:
            logger.info(f"Creating embedding for text: {text[:50]}...")
            vector = client.embeddings.create(text=text)
            logger.info("Embedding created successfully.")

            logger.info("Creating document in CosData...")
            doc = client.documents.create(
                content=text,
                metadata=metadata,
                embedding=vector.embedding
            )
            logger.info(f"Document created with ID: {doc.id}, Metadata: {metadata}")
            return doc.id
        except Exception as e:
            logger.error("CosData Cloud error, using local fallback.", exc_info=True)
    # Fallback: store locally
    doc_id = f"local_{len(_local_db)+1}"
    _local_db.append({"id": doc_id, "content": text, "metadata": metadata})
    logger.info(f"Fallback: Stored locally with ID: {doc_id}, Metadata: {metadata}")
    return doc_id

def search(query):
    client = get_client()
    if client:
        try:
            print(f"Querying CosData OSS with query: {query}")
            vector = client.embeddings.create(text=query)
            results = client.search.query(
                embedding=vector.embedding,
                top_k=5
            )
            print(f"Search results from CosData OSS: {results}")
            return results
        except Exception as e:
            print("CosData Cloud error, using local fallback.", e)
    # Fallback: naive local search
    print("Using fallback local search.")
    results = []
    for doc in _local_db:
        if query.lower() in doc["content"].lower():
            results.append(doc)
    print(f"Fallback search results: {results}")
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