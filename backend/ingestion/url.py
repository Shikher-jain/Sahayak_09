# backend/ingestion/url.py

import requests
from bs4 import BeautifulSoup
from backend.cosdata_client import CosDataClient

class URLIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()
        self.chunk_size = 500  # words per chunk

    def fetch_text(self, url):
        """Fetch page content and extract text"""
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch URL: {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ')
        return text

    def chunk_text(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks

    def ingest_url(self, url, metadata=None):
        """Fetch webpage, chunk text, generate embeddings, insert into Cosdata"""
        text = self.fetch_text(url)
        chunks = self.chunk_text(text)
        for idx, chunk in enumerate(chunks):
            meta = metadata.copy() if metadata else {}
            meta['chunk'] = idx
            meta['source_url'] = url
            self.cos_client.insert_vector(text=chunk, metadata=meta)
        print(f"Ingested {len(chunks)} chunks from URL: {url}")
