from fastapi import FastAPI, UploadFile, File, Form
from backend.ingestion.text import TextIngestor
from backend.ingestion.pdf import PDFIngestor
from backend.ingestion.image import ImageIngestor
from backend.ingestion.audio import AudioIngestor
from backend.ingestion.video import VideoIngestor

app = FastAPI(title="Sahayak Backend")

text_ingestor = TextIngestor()
pdf_ingestor = PDFIngestor()
image_ingestor = ImageIngestor()
audio_ingestor = AudioIngestor()
video_ingestor = VideoIngestor()


@app.post("/upload/text")
async def upload_text(text: str = Form(...)):
    text_ingestor.ingest_text(text)
    return {"status": "ok", "type": "text"}


@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    pdf_ingestor.ingest_pdf(path)
    return {"status": "ok", "type": "pdf"}


@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    image_ingestor.ingest_image(path)
    return {"status": "ok", "type": "image"}


@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    audio_ingestor.ingest_audio(path)
    return {"status": "ok", "type": "audio"}


@app.post("/upload/video")
async def upload_video(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    video_ingestor.ingest_video(path)
    return {"status": "ok", "type": "video"}
