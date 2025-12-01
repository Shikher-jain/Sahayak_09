# backend/ingestion/video.py

import os
from backend.cosdata_client import CosDataClient


class VideoIngestor:
    """
    Cloud-safe Video Ingestor
    Uses CosData SDK directly.
    No OpenCV, no FFmpeg – Compatible with Streamlit Cloud.
    """

    def __init__(self):
        self.client = CosDataClient()

    def ingest_video(self, video_path, metadata=None):
        """Send full video to CosData for transcription + embeddings."""
        import uuid
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        meta = metadata.copy() if metadata else {}
        meta["source"] = os.path.basename(video_path)
        if not meta.get('id') or not isinstance(meta.get('id'), str):
            meta['id'] = str(uuid.uuid4())

        with open(video_path, "rb") as f:
            video_bytes = f.read()

        response = self.client.ingest_video(video_bytes, metadata=meta)

        return {
            "status": "success",
            "message": "Video ingestion completed via CosData cloud.",
            "cosdata_response": response
        }
