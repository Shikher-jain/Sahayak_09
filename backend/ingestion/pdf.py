# backend/ingestion/pdf.py

import pdfplumber
from backend.cosdata_client import CosDataClient

class PDFIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()
        self.chunk_size = 500  # number of words per chunk

    def read_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def chunk_text(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks

    def ingest_pdf(self, pdf_path, metadata=None):
        """Read PDF, chunk text, generate embeddings, insert into Cosdata"""
        import uuid
        text = self.read_pdf(pdf_path)
        chunks = self.chunk_text(text)
        for idx, chunk in enumerate(chunks):
            meta = metadata.copy() if metadata else {}
            meta['chunk'] = idx
            # Ensure a unique string ID for each chunk
            if not meta.get('id') or not isinstance(meta.get('id'), str):
                meta['id'] = str(uuid.uuid4())
            self.cos_client.insert_vector(text=chunk, metadata=meta)
        print(f"Ingested {len(chunks)} chunks from {pdf_path}")
