# backend/ingestion/audio.py

import os
from backend.cosdata_client import CosDataClient

class AudioIngestor:
    def __init__(self):
        pass

    def ingest_audio(self, audio_path, metadata=None):
        """Insert audio file metadata into CosData (no local transcription)"""
        from backend.cosdata_client import insert_vector
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio not found: {audio_path}")

        meta = metadata.copy() if metadata else {}
        meta['source'] = os.path.basename(audio_path)
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        # For CosData, you may need to send audio as base64 or bytes, but here we use text placeholder
        doc_id = insert_vector("[AUDIO UPLOAD]", meta)
        print(f"Ingested audio: {audio_path}")
