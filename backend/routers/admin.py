from fastapi import APIRouter
from backend.db import list_uploaded_files

router = APIRouter()

@router.get("/admin/files")
def get_uploaded_files():
    files = list_uploaded_files()
    return {"files": files}
