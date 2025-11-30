
from fastapi import APIRouter, Request
from backend.services.vector_service import search_vectors
from backend.rag.search import RAGSearcher

router = APIRouter()
rag_searcher = RAGSearcher()

@router.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    results = search_vectors(query)
    return {"results": results}

# Add /rag/search endpoint for RAG-based semantic search
@router.post("/rag/search")
async def rag_search(request: Request):
    data = await request.json()
    query_text = data.get("query")
    top_k = data.get("top_k", 5)
    results = rag_searcher.query(query_text=query_text, top_k=top_k)
    return {"results": results}
