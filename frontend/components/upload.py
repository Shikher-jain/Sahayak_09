
# frontend/components/upload.py
import streamlit as st
import os, tempfile, requests

BACKEND_URL = "https://sahayak-09.onrender.com"

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
            with open(temp_path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/upload/pdf", files=files)
            if response.ok:
                st.success("PDF ingested successfully!")
            else:
                st.error("PDF ingestion failed!")

    elif upload_type == "Image":
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with open(temp_path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "image/png")}
                response = requests.post(f"{BACKEND_URL}/upload/image", files=files)
            if response.ok:
                st.success("Image ingested successfully!")
            else:
                st.error("Image ingestion failed!")

    elif upload_type == "URL":
        url = st.text_input("Enter URL")
        if url and st.button("Ingest URL"):
            response = requests.post(f"{BACKEND_URL}/upload/url", data={"url": url})
            if response.ok:
                st.success("URL ingested successfully!")
            else:
                st.error("URL ingestion failed!")

    elif upload_type == "Audio":
        uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with open(temp_path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "audio/wav")}
                response = requests.post(f"{BACKEND_URL}/upload/audio", files=files)
            if response.ok:
                st.success("Audio ingested successfully!")
            else:
                st.error("Audio ingestion failed!")

    elif upload_type == "Video":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        if uploaded_file:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with open(temp_path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "video/mp4")}
                response = requests.post(f"{BACKEND_URL}/upload/video", files=files)
            if response.ok:
                st.success("Video ingested successfully!")
            else:
                st.error("Video ingestion failed!")
