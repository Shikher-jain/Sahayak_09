# backend/ingestion/text.py
from backend.cosdata_client import CosDataClient

class TextIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()

    def ingest_text(self, text, metadata=None):
        """Generate embedding for text and insert into CosData/ChromaDB"""
        meta = metadata.copy() if metadata else {}
        self.cos_client.insert_vector(text=text, metadata=meta)
        print(f"Ingested text: {text[:50]}...")
