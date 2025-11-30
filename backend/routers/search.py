from fastapi import APIRouter, Request
from backend.services.vector_service import search_vectors

router = APIRouter()

@router.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    results = search_vectors(query)
    return {"results": results}
