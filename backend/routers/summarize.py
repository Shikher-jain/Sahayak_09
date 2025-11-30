from fastapi import APIRouter, Request
from backend.services.vector_service import summarize_text

router = APIRouter()

@router.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    text = data.get("text", "")
    summary = summarize_text(text)
    return {"summary": summary}
