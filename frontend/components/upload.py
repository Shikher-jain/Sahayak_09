# frontend/pip install moviepymponents/upload.py

import streamlit as st

import sys, os, tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.ingestion.pdf import PDFIngestor
from backend.ingestion.image import ImageIngestor
from backend.ingestion.url import URLIngestor
from backend.ingestion.audio import AudioIngestor
from backend.ingestion.video import VideoIngestor

def show_upload_ui():
    st.header("📁 Upload & Ingest Files")

    upload_type = st.selectbox("Select type to upload", ["PDF", "Image", "URL", "Audio", "Video"])


    if upload_type == "PDF":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            pdf_ingestor = PDFIngestor()
            pdf_ingestor.ingest_pdf(temp_path)
            st.success("PDF ingested successfully!")

    elif upload_type == "Image":
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            image_ingestor = ImageIngestor()
            image_ingestor.ingest_image(temp_path)
            st.success("Image ingested successfully!")

    elif upload_type == "URL":
        url = st.text_input("Enter URL")
        if url and st.button("Ingest URL"):
            url_ingestor = URLIngestor()
            url_ingestor.ingest_url(url)
            st.success("URL ingested successfully!")

    elif upload_type == "Audio":
        uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            audio_ingestor = AudioIngestor()
            audio_ingestor.ingest_audio(temp_path)
            st.success("Audio ingested successfully!")

    elif upload_type == "Video":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            video_ingestor = VideoIngestor()
            video_ingestor.ingest_video(temp_path)
            st.success("Video ingested successfully!")
