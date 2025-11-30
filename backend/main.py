
from fastapi import FastAPI
from backend.routers import ingestion, search, summarize

app = FastAPI(title="Sahayak Backend")

app.include_router(ingestion.router)
app.include_router(search.router)
app.include_router(summarize.router)

