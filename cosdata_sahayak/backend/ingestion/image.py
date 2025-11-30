# backend/ingestion/image.py

from backend.cosdata_client import CosDataClient
from PIL import Image
import os

class ImageIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()

    def ingest_image(self, image_path, metadata=None):
        """Generate embedding for an image and insert into Cosdata"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        meta = metadata.copy() if metadata else {}
        meta['source'] = os.path.basename(image_path)
        self.cos_client.insert_vector(image_path=image_path, metadata=meta)
        print(f"Ingested image: {image_path}")
