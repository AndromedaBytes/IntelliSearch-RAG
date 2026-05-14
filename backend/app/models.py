from pydantic import BaseModel
from typing import List, Optional


class Citation(BaseModel):
    """Citation model for answer references"""
    source: str
    type: str
    chunk_id: int
    similarity_score: float


class IngestResponse(BaseModel):
    """Response model for file ingestion"""
    status: str
    filename: str
    chunks_stored: int
    file_type: str


class QueryRequest(BaseModel):
    """Request model for queries"""
    query: str
    similarity_threshold: float | None = None
    full_document_mode: bool = False


class QueryResponse(BaseModel):
    """Response model for queries"""
    answer: str
    citations: List[Citation] = []
    top_similarity: float
    gate_passed: bool
    model_used: str
    auto_full_document_enabled: bool = False


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    chromadb_connected: bool
    corpus_size: int
    models: dict


class CorpusFile(BaseModel):
    """Model for a file in corpus"""
    filename: str
    file_type: str
    chunk_count: int
    upload_date: str


class CorpusInfo(BaseModel):
    """Response model for corpus information"""
    total_documents: int
    files: List[CorpusFile] = []


class DeleteResponse(BaseModel):
    """Response model for delete operations"""
    status: str
    deleted_count: int
    remaining_documents: int
