# backend/ingestion/audio.py

import os
import tempfile
import torch
import torchaudio
from backend.cosdata_client import CosDataClient
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class AudioIngestor:
    def __init__(self):
        self.cos_client = CosDataClient()

        # Load HuggingFace Wav2Vec2 model for STT
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(self.device)

    def transcribe_audio(self, audio_path):
        """Convert audio file to text"""
        waveform, sample_rate = torchaudio.load(audio_path)
        waveform = waveform.squeeze(0)
        inputs = self.processor(waveform, sampling_rate=sample_rate, return_tensors="pt", padding=True).input_values.to(self.device)
        with torch.no_grad():
            logits = self.model(inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription

    def ingest_audio(self, audio_path, metadata=None):
        """Generate embeddings for audio transcription and insert into Cosdata"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio not found: {audio_path}")

        meta = metadata.copy() if metadata else {}
        meta['source'] = os.path.basename(audio_path)

        # Transcribe audio
        text = self.transcribe_audio(audio_path)

        # Insert into Cosdata
        self.cos_client.insert_vector(text=text, metadata=meta)
        print(f"Ingested audio: {audio_path} with transcription")
