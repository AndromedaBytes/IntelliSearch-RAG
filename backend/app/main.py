"""
IntelliSearch V2 - FastAPI main application
Dual-Brain Cloud-Hybrid Multimodal RAG Platform
"""

import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import openai

from backend.app.config import settings
from backend.app.models import HealthResponse
from backend.app.routers.ingest import ingest_router
from backend.app.routers.query import query_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    # Startup
    logger.info("IntelliSearch V2 online")
    try:
        from backend.app.services.chromadb_service import chroma_service
        corpus_size = chroma_service.get_corpus_size()
        logger.info(f"ChromaDB connected | Corpus size: {corpus_size} documents")
    except Exception as e:
        logger.warning(f"ChromaDB connection warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("IntelliSearch V2 shutdown")


# Create FastAPI app
app = FastAPI(
    title="IntelliSearch V2",
    version="2.0.0",
    description="Cloud-Hybrid Multimodal RAG Platform",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*", "X-IntelliSearch-Client-Key"],
)


# Exception Handlers
@app.exception_handler(openai.RateLimitError)
async def rate_limit_handler(request: Request, exc: openai.RateLimitError):
    """Handle OpenAI rate limit errors"""
    logger.warning(f"Rate limit exceeded: {exc}")
    return JSONResponse(
        status_code=429,
        content={"error": "rate_limit", "message": "API rate limit exceeded. Please try again later."}
    )


@app.exception_handler(openai.AuthenticationError)
async def auth_error_handler(request: Request, exc: openai.AuthenticationError):
    """Handle OpenAI authentication errors"""
    logger.error(f"Authentication failed: {exc}")
    return JSONResponse(
        status_code=401,
        content={"error": "auth_failed", "message": "GitHub Models authentication failed. Check your tokens."}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions"""
    logger.error(f"Internal error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "message": "An unexpected error occurred."}
    )


# Health Check Endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - no authentication required for monitoring
    """
    try:
        from backend.app.services.chromadb_service import chroma_service
        corpus_size = chroma_service.get_corpus_size()
        chromadb_connected = True
    except Exception as e:
        logger.warning(f"ChromaDB health check failed: {e}")
        corpus_size = 0
        chromadb_connected = False
    
    return HealthResponse(
        status="ok",
        chromadb_connected=chromadb_connected,
        corpus_size=corpus_size,
        models={
            "gpt4o": settings.GPT4O_MODEL,
            "llama": settings.LLAMA_MODEL,
            "github_models": settings.GITHUB_MODELS_BASE_URL
        }
    )


# Include routers
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
app.include_router(query_router, prefix="/query", tags=["query"])


# Serve the exported frontend at the root when available.
frontend_out = Path(__file__).resolve().parents[2] / "frontend" / "out"
if frontend_out.exists():
    app.mount("/", StaticFiles(directory=str(frontend_out), html=True), name="frontend")
else:
    logger.warning(f"Frontend bundle not found at {frontend_out}; root requests will return 404")
