from fastapi import APIRouter, UploadFile, File, Form
from backend.services.pdf_service import ingest_pdf
from backend.services.image_service import ingest_image
from backend.services.audio_service import ingest_audio
from backend.services.vector_service import ingest_text
from backend.db import save_file_metadata

router = APIRouter()

@router.post("/upload/text")
async def upload_text(text: str = Form(...)):
    ingest_text(text)
    return {"status": "ok", "type": "text"}

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    ingest_pdf(path)
    save_file_metadata(file.filename, "pdf", "user")
    return {"status": "ok", "type": "pdf"}

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    ingest_image(path)
    save_file_metadata(file.filename, "image", "user")
    return {"status": "ok", "type": "image"}

@router.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    ingest_audio(path)
    save_file_metadata(file.filename, "audio", "user")
    return {"status": "ok", "type": "audio"}
