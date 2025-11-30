# backend/ingestion/video.py

import os
import tempfile
import cv2
import ffmpeg
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

        # Extract audio using ffmpeg
        audio_path = tempfile.mktemp(suffix=".wav")
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"Extracted audio: {audio_path}")
        self.audio_ingestor.ingest_audio(audio_path, metadata=meta)
        os.remove(audio_path)

        # Extract keyframes using OpenCV
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(frame_count / fps) if fps else 0
        for t in range(0, duration, self.frame_interval):
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = cap.read()
            if ret:
                frame_path = tempfile.mktemp(suffix=".png")
                from PIL import Image
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img.save(frame_path)
                self.image_ingestor.ingest_image(frame_path, metadata=meta)
                os.remove(frame_path)
        cap.release()

        print(f"Ingested video: {video_path} with audio + keyframes")
