"""
Ingest endpoint tests for IntelliSearch V2
"""

import pytest
from httpx import AsyncClient
from io import BytesIO
import os

from backend.app.main import app
from backend.app.config import settings
from backend.app.services.chromadb_service import chroma_service


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test GET /health endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "chromadb_connected" in data
        assert "corpus_size" in data
        assert "models" in data


@pytest.mark.asyncio
async def test_ingest_without_client_key(sample_pdf_bytes):
    """Test ingest without client key returns 403"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/ingest/",
            files={"file": ("test.pdf", sample_pdf_bytes)}
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_ingest_invalid_client_key(sample_pdf_bytes):
    """Test ingest with invalid client key returns 403"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/ingest/",
            files={"file": ("test.pdf", sample_pdf_bytes)},
            headers={"X-IntelliSearch-Client-Key": "invalid-key"}
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_ingest_unsupported_filetype(valid_client_key):
    """Test ingest with unsupported file type returns 415"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/ingest/",
            files={"file": ("test.txt", b"some text content")},
            headers={"X-IntelliSearch-Client-Key": valid_client_key}
        )
        assert response.status_code == 415


def test_chunk_text_preserves_short_audio_transcript():
    """Short audio transcripts should still become searchable corpus chunks."""
    chunks = chroma_service.chunk_text("Short but meaningful audio note.")
    assert chunks == ["Short but meaningful audio note."]


@pytest.mark.asyncio
async def test_query_without_client_key():
    """Test query without client key returns 403"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/query/",
            json={"query": "test question"}
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_query_invalid_client_key():
    """Test query with invalid client key returns 403"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/query/",
            json={"query": "test question"},
            headers={"X-IntelliSearch-Client-Key": "invalid-key"}
        )
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_query_empty_string(valid_client_key):
    """Test query with empty string returns 400"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/query/",
            json={"query": ""},
            headers={"X-IntelliSearch-Client-Key": valid_client_key}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_query_too_long(valid_client_key):
    """Test query over 2000 chars returns 400"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        long_query = "x" * 2001
        response = await client.post(
            "/query/",
            json={"query": long_query},
            headers={"X-IntelliSearch-Client-Key": valid_client_key}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_query_empty_corpus(valid_client_key):
    """Test query on empty corpus returns gate_blocked response"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/query/",
            json={"query": "What is machine learning?"},
            headers={"X-IntelliSearch-Client-Key": valid_client_key}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["gate_passed"] is False
        assert "No documents have been ingested" in data["answer"]
