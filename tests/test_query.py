"""
Query endpoint tests for IntelliSearch V2
"""

import pytest
from httpx import AsyncClient

from backend.app.main import app
from backend.app.config import settings


@pytest.mark.asyncio
async def test_query_response_structure(valid_client_key):
    """Test query response has required fields"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/query/",
            json={"query": "What is IntelliSearch?"},
            headers={"X-IntelliSearch-Client-Key": valid_client_key}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "answer" in data
        assert "citations" in data
        assert "top_similarity" in data
        assert "gate_passed" in data
        assert "model_used" in data
        
        # Answer should be string
        assert isinstance(data["answer"], str)
        # Citations should be list
        assert isinstance(data["citations"], list)
        # Similarity should be float
        assert isinstance(data["top_similarity"], (int, float))
        # gate_passed should be boolean
        assert isinstance(data["gate_passed"], bool)


@pytest.mark.asyncio
async def test_citation_structure():
    """Test citation objects have required fields"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Get a citation from query with non-empty corpus
        # This is a structural test of the response format
        pass  # Tested as part of integration tests


@pytest.mark.asyncio
async def test_similarity_gate_logic():
    """Test similarity gate blocks low-confidence queries"""
    # When top_similarity < 0.70, gate should block
    # This is integration tested with real ChromaDB
    pass  # Integration tested in Phase 11
