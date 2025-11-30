# backend/cosdata_client.py

import os
from cosdata import Client
from sentence_transformers import SentenceTransformer
from PIL import Image
import numpy as np

class CosDataClient:
    def __init__(self):
        # Cosdata connection
        self.client = Client(
            host=os.environ.get("COSDATA_HOST"),
            username=os.environ.get("COSDATA_USER"),
            password=os.environ.get("COSDATA_PASS"),
            verify=True
        )
        self.collection = self.client.get_or_create_collection(
            name="multimodal_knowledge",
            dimension=384  # default MiniLM dimension
        )

        # HuggingFace models
        self.text_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.image_model = SentenceTransformer('clip-ViT-B-32')  # CLIP embeddings

    def embed_text(self, text: str):
        return self.text_model.encode(text).tolist()

    def embed_image(self, image_path: str):
        image = Image.open(image_path).convert('RGB')
        return self.image_model.encode([image])[0].tolist()

    def insert_vector(self, text=None, image_path=None, metadata=None):
        """Insert text or image embedding into Cosdata"""
        vector = None
        if text:
            vector = self.embed_text(text)
        elif image_path:
            vector = self.embed_image(image_path)
        else:
            raise ValueError("Either text or image_path must be provided")

        vector_id = metadata.get("id") if metadata and "id" in metadata else None
        self.collection.upsert_vector({
            "id": vector_id,
            "dense_values": vector,
            "text": text or "",
            "metadata": metadata or {}
        })

    def query_vectors(self, query_text=None, query_image_path=None, top_k=5):
        """Query Cosdata with text or image"""
        vector = None
        if query_text:
            vector = self.embed_text(query_text)
        elif query_image_path:
            vector = self.embed_image(query_image_path)
        else:
            raise ValueError("Either query_text or query_image_path must be provided")

        results = self.collection.search.dense(
            query_vector=vector,
            top_k=top_k,
            return_raw_text=True
        )
        return results
