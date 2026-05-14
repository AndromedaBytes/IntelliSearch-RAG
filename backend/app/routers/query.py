"""
Query router - POST /query endpoint
Performs RAG query with similarity gate and citation mapping
"""

from fastapi import APIRouter, Depends, HTTPException
import logging
import time
from typing import Set

from backend.app.security import verify_client_key
from backend.app.models import QueryRequest, QueryResponse, Citation, CorpusInfo, CorpusFile, DeleteResponse
from backend.app.config import settings
from backend.app.services.chromadb_service import chroma_service
from backend.app.services.llama_service import llama_service

logger = logging.getLogger(__name__)

query_router = APIRouter()


@query_router.post("/", response_model=QueryResponse)
async def query_corpus(
    request: QueryRequest,
    client_key: str = Depends(verify_client_key)
) -> QueryResponse:
    """
    Query the ingested corpus with RAG pipeline and similarity scoring.
    
    Similarity now acts as a confidence signal instead of a hard block.
    The model always receives context so an answer is returned even when
    the closest match is weak. When full_document_mode is enabled, the model
    receives every ingested chunk instead of only the top-k retrieval set.
    
    Pipeline:
    1. Validate input
    2. Retrieve top-k chunks from ChromaDB
    3. THE SIMILARITY GATE - blocks if top_similarity < 0.70
    4. Llama synthesis (only if gate passes)
    5. Citation extraction and deduplication
    6. Return response
    """
    start_time = time.time()
    
    try:
        # STEP 1: Validate input
        query = request.query.strip()
        
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long (max 2000 characters)")
        
        logger.info(f"Query received: {query[:100]}...")
        
        full_document_mode = request.full_document_mode
        auto_enabled = False
        
        # Auto-enable full-document mode if exactly one PDF is in corpus
        if not full_document_mode and chroma_service.has_single_pdf():
            full_document_mode = True
            auto_enabled = True
            logger.info("Auto-enabled full-document mode for single PDF corpus")

        # STEP 2: ChromaDB Retrieval
        results = chroma_service.query_corpus(
            query,
            top_k=settings.TOP_K_RETRIEVAL
        )
        
        corpus_size = chroma_service.get_corpus_size()
        
        if corpus_size == 0:
            logger.info("Corpus is empty")
            return QueryResponse(
                answer="No documents have been ingested yet. Please upload files first.",
                citations=[],
                top_similarity=0.0,
                gate_passed=False,
                model_used="gate_empty_corpus",
                auto_full_document_enabled=False
            )
        
        # STEP 3: Similarity score as a confidence signal
        top_similarity = results["top_similarity"]

        # Allow client-side override of the similarity threshold if provided
        threshold = request.similarity_threshold if request.similarity_threshold is not None else settings.SIMILARITY_THRESHOLD
        if top_similarity < threshold:
            logger.warning(
                f"Low confidence retrieval: top similarity {top_similarity:.3f} < "
                f"{threshold} (threshold)"
            )
        else:
            logger.info(f"Confidence OK: top similarity {top_similarity:.3f} >= {threshold}")
        
        if full_document_mode:
            full_corpus = chroma_service.get_all_documents()
            context_chunks = full_corpus["chunks"]
            context_metadatas = full_corpus["metadatas"]
            logger.info(
                f"Full-document mode enabled | Context chunks: {len(context_chunks)} | "
                f"Top similarity: {top_similarity:.3f}"
            )
        else:
            context_chunks = results["chunks"]
            context_metadatas = results["metadatas"]

        # STEP 4: Llama synthesis always runs so an answer is returned
        answer = await llama_service.synthesize(
            query,
            context_chunks,
            context_metadatas
        )
        
        # STEP 5: Citation Extraction and Deduplication
        citations_dict: dict[str, Citation] = {}
        
        for meta, similarity_score in zip(results["metadatas"], results["similarities"]):
            source = meta.get("source", "unknown")
            file_type = meta.get("type", "unknown")
            chunk_idx = meta.get("chunk_index", 0)
            
            # Deduplicate by source - keep highest similarity
            if source not in citations_dict or similarity_score > citations_dict[source].similarity_score:
                citations_dict[source] = Citation(
                    source=source,
                    type=file_type,
                    chunk_id=chunk_idx,
                    similarity_score=similarity_score
                )
        
        # Sort by similarity descending
        citations = sorted(
            citations_dict.values(),
            key=lambda c: c.similarity_score,
            reverse=True
        )
        
        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            f"Query complete | Latency: {elapsed_ms:.0f}ms | "
            f"Citations: {len(citations)} | Top similarity: {top_similarity:.3f}"
        )
        
        # STEP 6: Return response
        return QueryResponse(
            answer=answer,
            citations=citations,
            top_similarity=top_similarity,
            gate_passed=True,
            model_used=settings.LLAMA_MODEL,
            auto_full_document_enabled=auto_enabled
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )


@query_router.get("/corpus/info", response_model=CorpusInfo)
async def get_corpus_info(
    client_key: str = Depends(verify_client_key)
) -> CorpusInfo:
    """
    Get information about all files in corpus.
    Returns list of ingested files with metadata.
    """
    try:
        sources = chroma_service.get_all_sources()
        files = [
            CorpusFile(
                filename=s["filename"],
                file_type=s["file_type"],
                chunk_count=s["chunk_count"],
                upload_date=s["upload_date"]
            )
            for s in sources
        ]
        total_docs = chroma_service.get_corpus_size()
        
        logger.info(f"Corpus info requested: {len(files)} files, {total_docs} total documents")
        
        return CorpusInfo(
            total_documents=total_docs,
            files=files
        )
    
    except Exception as e:
        logger.error(f"Failed to get corpus info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Corpus info retrieval failed: {str(e)}")


@query_router.delete("/corpus/files/{filename}", response_model=DeleteResponse)
async def delete_corpus_file(
    filename: str,
    client_key: str = Depends(verify_client_key)
) -> DeleteResponse:
    """
    Delete a specific file and all its chunks from corpus.
    """
    try:
        # Delete the file
        deleted_count = chroma_service.delete_source(filename)
        remaining = chroma_service.get_corpus_size()
        
        if deleted_count == 0:
            logger.warning(f"File not found: {filename}")
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found in corpus")
        
        logger.info(f"Deleted file {filename}: {deleted_count} chunks removed, {remaining} remain")
        
        return DeleteResponse(
            status="success",
            deleted_count=deleted_count,
            remaining_documents=remaining
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete file {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"File deletion error: {str(e)}")


@query_router.delete("/corpus", response_model=DeleteResponse)
async def clear_corpus(
    client_key: str = Depends(verify_client_key)
) -> DeleteResponse:
    """
    Clear entire corpus - deletes all documents.
    WARNING: This is irreversible.
    """
    try:
        deleted_count = chroma_service.clear_corpus()
        remaining = chroma_service.get_corpus_size()
        
        logger.warning(f"Corpus cleared: {deleted_count} documents removed, {remaining} remaining")
        
        return DeleteResponse(
            status="success",
            deleted_count=deleted_count,
            remaining_documents=remaining
        )
    
    except Exception as e:
        logger.error(f"Failed to clear corpus: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Corpus clear error: {str(e)}")

