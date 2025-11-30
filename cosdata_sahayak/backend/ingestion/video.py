# backend/ingestion/video.py

import os
import tempfile
from moviepy.editor import VideoFileClip
from backend.cosdata_client import CosDataClient
from backend.ingestion.audio import AudioIngestor
from backend.ingestion.image import ImageIngestor

class VideoIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()
        self.audio_ingestor = AudioIngestor()
        self.image_ingestor = ImageIngestor()
        self.frame_interval = 5  # extract keyframe every 5 seconds

    def ingest_video(self, video_path, metadata=None):
        """Extract audio + keyframes, generate embeddings, insert into Cosdata"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        meta = metadata.copy() if metadata else {}
        meta['source'] = os.path.basename(video_path)

        clip = VideoFileClip(video_path)

        # Extract audio to temporary file
        audio_path = tempfile.mktemp(suffix=".wav")
        clip.audio.write_audiofile(audio_path, logger=None)
        print(f"Extracted audio: {audio_path}")
        # Ingest audio embeddings
        self.audio_ingestor.ingest_audio(audio_path, metadata=meta)
        os.remove(audio_path)

        # Extract keyframes at interval
        duration = int(clip.duration)
        for t in range(0, duration, self.frame_interval):
            frame = clip.get_frame(t)
            # Save frame temporarily
            frame_path = tempfile.mktemp(suffix=".png")
            from PIL import Image
            img = Image.fromarray(frame)
            img.save(frame_path)
            self.image_ingestor.ingest_image(frame_path, metadata=meta)
            os.remove(frame_path)

        print(f"Ingested video: {video_path} with audio + keyframes")
