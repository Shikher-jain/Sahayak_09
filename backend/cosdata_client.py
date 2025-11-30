# backend/cosdata_client.py

import os
from cosdata import Client
from sentence_transformers import SentenceTransformer
from PIL import Image

class CosDataClient:
    def __init__(self):
        # Cloud-safe API host
        host = os.getenv("COSDATA_HOST", "https://api.cosdata.io")

        # API Key authentication (the correct method)
        api_key = os.getenv("COSDATA_API_KEY")

        if not api_key:
            raise ValueError(
                "COSDATA_API_KEY is missing. "
                "Add it inside Streamlit → Settings → Secrets."
            )

        # Initialize CosData client
        self.client = Client(
            host=host,
            api_key=api_key,
            verify=False        # IMPORTANT: Fixes SSL errors on Streamlit Cloud
        )

        # Create collection once
        self.collection = self.client.get_or_create_collection(
            name="multimodal_knowledge",
            dimension=384       # MiniLM dimension
        )

        # Lazy loading (faster startup)
        self.text_model = None
        self.image_model = None

    # -------------------------------
    #   HF Model Loaders
    # -------------------------------
    def load_text_model(self):
        if self.text_model is None:
            self.text_model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        return self.text_model

    def load_image_model(self):
        if self.image_model is None:
            self.image_model = SentenceTransformer("clip-ViT-B-32")
        return self.image_model

    # -------------------------------
    #   Embedding Functions
    # -------------------------------
    def embed_text(self, text: str):
        model = self.load_text_model()
        return model.encode(text).tolist()

    def embed_image(self, image_path: str):
        model = self.load_image_model()
        img = Image.open(image_path).convert("RGB")
        return model.encode([img])[0].tolist()

    # -------------------------------
    #   Insert Vector into CosData
    # -------------------------------
    def insert_vector(self, text=None, image_path=None, metadata=None):
        if not metadata:
            metadata = {}

        if text:
            vector = self.embed_text(text)
        elif image_path:
            vector = self.embed_image(image_path)
        else:
            raise ValueError("Either text or image_path must be provided")

        self.collection.upsert_vector({
            "id": metadata.get("id"),
            "dense_values": vector,
            "text": text or "",
            "metadata": metadata
        })

    # -------------------------------
    #   Query CosData
    # -------------------------------
    def query_vectors(self, query_text=None, query_image_path=None, top_k=5):
        if query_text:
            vector = self.embed_text(query_text)
        elif query_image_path:
            vector = self.embed_image(query_image_path)
        else:
            raise ValueError("Either query_text or query_image_path must be provided")

        return self.collection.search.dense(
            query_vector=vector,
            top_k=top_k,
            return_raw_text=True
        )

    # -------------------------------
    #   Video / Audio Ingestion (SDK)
    # -------------------------------
    def ingest_video(self, video_bytes, metadata=None):
        return self.client.ingest.video(
            file_bytes=video_bytes,
            metadata=metadata or {}
        )

    def ingest_audio(self, audio_bytes, metadata=None):
        return self.client.ingest.audio(
            file_bytes=audio_bytes,
            metadata=metadata or {}
        )

    def ingest_image(self, image_bytes, metadata=None):
        return self.client.ingest.image(
            file_bytes=image_bytes,
            metadata=metadata or {}
        )
