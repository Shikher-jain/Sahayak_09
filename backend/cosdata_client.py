import os
from backend.cosdata_config import COSDATA_HOST, COSDATA_USER, COSDATA_PASS
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image

USE_COSDATA = os.environ.get("COSDATA_ENABLED", "false").lower() == "true"

if USE_COSDATA:
    from cosdata import Client
else:
    import chromadb
    from chromadb.config import Settings


class CosDataClient:
    def __init__(self):

        # Embedding models
        self.text_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.image_model = SentenceTransformer('clip-ViT-B-32')

        if USE_COSDATA:
            print("🔗 Using CosData Cloud")
            host = COSDATA_HOST
            username = COSDATA_USER
            password = COSDATA_PASS

            self.client = Client(
                host=host,
                username=username,
                password=password,
                verify=True
            )

            self.collection = self.client.get_or_create_collection(
                name="multimodal_knowledge",
                dimension=384
            )

        else:
            print("💾 Using Local ChromaDB (No API key required)")
            self.client = chromadb.PersistentClient(path="./chromadb_data")
            self.collection = self.client.get_or_create_collection(
                name="multimodal_local"
            )

    def embed_text(self, text):
        return self.text_model.encode(text).tolist()

    def embed_image(self, path):
        img = Image.open(path).convert('RGB')
        return self.image_model.encode([img])[0].tolist()

    def insert_vector(self, text=None, image_path=None, metadata=None):
        import uuid
        if text:
            vector = self.embed_text(text)
        elif image_path:
            vector = self.embed_image(image_path)
        else:
            raise ValueError("Either text or image_path must be provided")

        if metadata is None:
            metadata = {}
        vector_id = metadata.get("id")
        if not vector_id or not isinstance(vector_id, str):
            vector_id = str(uuid.uuid4())
            metadata["id"] = vector_id

        if USE_COSDATA:
            self.collection.upsert_vector({
                "id": vector_id,
                "dense_values": vector,
                "text": text or "",
                "metadata": metadata,
            })
        else:
            self.collection.add(
                ids=[vector_id],
                embeddings=[vector],
                metadatas=[metadata],
                documents=[text or ""]
            )

    def query_vectors(self, query_text=None, query_image_path=None, top_k=5):
        if query_text:
            vector = self.embed_text(query_text)
        else:
            vector = self.embed_image(query_image_path)

        if USE_COSDATA:
            return self.collection.search.dense(
                query_vector=vector,
                top_k=top_k,
                return_raw_text=True
            )

        else:
            return self.collection.query(
                query_embeddings=[vector],
                n_results=top_k
            )
