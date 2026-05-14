import sys
import pathlib

# Ensure project root is on sys.path
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.app.services.chromadb_service import chroma_service

chunks = [
    "This is a sample test document about Project Xeno. It contains information about installation, setup, and usage. "
    "Use this document to verify search and retrieval pipelines. It mentions the keyword 'Xeno' multiple times for testing purposes.",
    "Additional context: contact the dev team at dev@example.com. The system supports PDF, images, and audio ingestion."
]

count = chroma_service.store_chunks(chunks, source="manual_test.txt", file_type="text")
print("STORED", count)
