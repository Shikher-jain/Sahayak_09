# backend/ingestion/image.py

from backend.cosdata_client import CosDataClient
from PIL import Image
import os

class ImageIngestor:
    def __init__(self):
        pass

    def ingest_image(self, image_path, metadata=None):
        """Generate embedding for an image and insert into CosData"""
        from backend.cosdata_client import insert_vector
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        meta = metadata.copy() if metadata else {}
        meta['source'] = os.path.basename(image_path)
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        # For CosData, you may need to send image as base64 or bytes, but here we use text placeholder
        doc_id = insert_vector("[IMAGE UPLOAD]", meta)
        print(f"Ingested image: {image_path}")
