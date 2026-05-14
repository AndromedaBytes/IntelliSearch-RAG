"""
File ingestion router - POST /ingest endpoint
Accepts multimodal files (PDF, images, audio) and stores in ChromaDB
"""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import logging
import time

from backend.app.security import verify_client_key
from backend.app.models import IngestResponse
from backend.app.services.chromadb_service import chroma_service
from backend.app.services.gpt4o_service import gpt4o_service

logger = logging.getLogger(__name__)

ingest_router = APIRouter()


@ingest_router.post("/", response_model=IngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    client_key: str = Depends(verify_client_key)
) -> IngestResponse:
    """
    Ingest a multimodal file (PDF, image, or audio).
    Extracts semantic text via GPT-4o and stores in ChromaDB.
    
    Supported formats:
    - PDF: .pdf
    - Images: .png, .jpg, .jpeg, .webp
    - Audio: .mp3, .wav, .ogg, .m4a
    """
    start_time = time.time()
    
    try:
        # Read file contents
        content = await file.read()
        file_size_kb = len(content) / 1024
        
        logger.info(f"Ingesting file: {file.filename} ({file_size_kb:.1f} KB)")
        
        # Detect file type by extension
        filename_lower = file.filename.lower()
        
        if filename_lower.endswith('.pdf'):
            file_type = 'pdf'
            extracted_text = await gpt4o_service.extract_from_pdf(content, file.filename)
        
        elif filename_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            file_type = 'image'
            extracted_text = await gpt4o_service.extract_from_image(content, file.filename)
        
        elif filename_lower.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
            file_type = 'audio'
            extracted_text = await gpt4o_service.extract_from_audio(content, file.filename)
        
        else:
            logger.error(f"Unsupported file type: {file.filename}")
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type. Supported: PDF, PNG, JPG, JPEG, WEBP, MP3, WAV, OGG, M4A"
            )
        
        # Chunk extracted text
        chunks = chroma_service.chunk_text(extracted_text)
        if not chunks:
            logger.warning(f"No searchable text extracted from {file.filename}")
            raise HTTPException(
                status_code=422,
                detail="No searchable text could be extracted from this file."
            )
        
        # Store chunks in ChromaDB
        chunks_stored = chroma_service.store_chunks(chunks, file.filename, file_type)
        if chunks_stored == 0:
            logger.error(f"ChromaDB stored zero chunks for {file.filename}")
            raise HTTPException(
                status_code=500,
                detail="File text was extracted, but no chunks were stored."
            )
        
        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            f"Ingest complete | {file.filename} | "
            f"Chunks: {chunks_stored} | Latency: {elapsed_ms:.0f}ms"
        )
        
        return IngestResponse(
            status="success",
            filename=file.filename,
            chunks_stored=chunks_stored,
            file_type=file_type
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"File ingestion error: {str(e)}"
        )

