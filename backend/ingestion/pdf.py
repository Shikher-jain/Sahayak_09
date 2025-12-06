# backend/ingestion/pdf.py

import pdfplumber
from backend.rag.embedder import Embedder

def ingest_pdf(pdf_path, cosdata_client):
    embedder = Embedder()
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    chunks = chunk_text(text)
    for chunk in chunks:
        vector = embedder.embed_text(chunk)
        vector_id = embedder.generate_id()
        metadata = {"source": pdf_path, "chunk": chunk[:30]}
        cosdata_client.insert_vector(vector_id, vector, metadata)

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
