

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.routers import ingestion, search, summarize
from backend.routers import admin
import logging

app = FastAPI(title="Sahayak Backend")

# CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sahayak-backend")

# Health check endpoints
@app.get("/")
def root():
	return {"status": "ok"}

@app.get("/health")
def health_check():
	return {"status": "healthy"}

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	logger.error(f"Unhandled error: {exc}")
	return JSONResponse(status_code=500, content={"detail": str(exc)})

# Routers
app.include_router(ingestion.router)
app.include_router(search.router)
app.include_router(summarize.router)
app.include_router(admin.router)

# Startup event
@app.on_event("startup")
async def startup_event():
	logger.info("Sahayak Backend starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
	logger.info("Sahayak Backend shutting down...")

