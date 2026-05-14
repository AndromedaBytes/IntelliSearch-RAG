"""
ChromaDB Service - Vector database layer for IntelliSearch V2
Handles local persistent vector embeddings, chunking, and similarity search
"""

import chromadb
from typing import List, Dict, Any
import logging
from datetime import datetime

from backend.app.config import settings

logger = logging.getLogger(__name__)


class ChromaDBService:
    """Service for managing ChromaDB vector database operations"""
    
    def __init__(self):
        """Initialize ChromaDB persistent client and collection"""
        try:
            self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"ChromaDB initialized at {settings.CHROMA_PERSIST_DIR}")
        except Exception as e:
            logger.error(f"ChromaDB initialization failed: {e}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into overlapping chunks without breaking words.
        
        Args:
            text: Text to chunk
            chunk_size: Characters per chunk (default: settings.CHUNK_SIZE)
            overlap: Overlap between chunks (default: settings.CHUNK_OVERLAP)
            
        Returns:
            List of clean chunk strings, minimum 50 chars each
        """
        if chunk_size is None:
            chunk_size = settings.CHUNK_SIZE
        if overlap is None:
            overlap = settings.CHUNK_OVERLAP
        
        text = text.strip()
        if not text:
            logger.warning("No text provided for chunking")
            return []

        if len(text) < 50:
            logger.info("Text shorter than minimum chunk length; preserving as one chunk")
            return [text]

        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # If we're not at the end, find a word boundary
            if end < len(text):
                # Look for the nearest space
                while end > start and text[end] not in (' ', '\n', '\t', '.', ',', ';'):
                    end -= 1
                # If we couldn't find a boundary, use the hard limit
                if end == start:
                    end = min(start + chunk_size, len(text))
            
            chunk = text[start:end].strip()
            
            # Only include chunks with sufficient content
            if len(chunk) >= 50:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap if end < len(text) else end
        
        logger.info(f"Chunked text into {len(chunks)} pieces (size={chunk_size}, overlap={overlap})")
        return chunks
    
    def store_chunks(self, chunks: List[str], source: str, file_type: str) -> int:
        """
        Store text chunks in ChromaDB with full metadata.
        
        Args:
            chunks: List of text chunks
            source: Source filename/identifier
            file_type: Type of file (pdf, image, audio, etc)
            
        Returns:
            Count of chunks stored
        """
        if not chunks:
            logger.warning(f"No chunks to store for {source}")
            return 0
        
        # Delete existing chunks from same source (deduplication)
        try:
            self.collection.delete(
                where={"source": source},
                where_document={}
            )
            logger.info(f"Cleaned previous chunks for {source}")
        except Exception as e:
            logger.debug(f"No previous chunks to clean: {e}")
        
        # Prepare chunk data
        chunk_ids = []
        metadatas = []
        documents = []
        
        for i, chunk in enumerate(chunks):
            chunk_ids.append(f"{source}_chunk_{i}")
            metadatas.append({
                "source": source,
                "type": file_type,
                "chunk_index": i,
                "timestamp": datetime.utcnow().isoformat(),
                "total_chunks": len(chunks)
            })
            documents.append(chunk)
        
        # Store in batches of 50 to avoid memory issues
        batch_size = 50
        for i in range(0, len(chunk_ids), batch_size):
            batch_end = min(i + batch_size, len(chunk_ids))
            self.collection.add(
                ids=chunk_ids[i:batch_end],
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )
            logger.debug(f"Stored batch {i // batch_size + 1} for {source}")
        
        logger.info(f"Stored {len(chunks)} chunks for {source} ({file_type})")
        return len(chunks)
    
    def query_corpus(self, query: str, top_k: int = None) -> Dict[str, Any]:
        """
        Query corpus and return top-k most similar chunks.
        
        Args:
            query: Query text
            top_k: Number of results to return (default: settings.TOP_K_RETRIEVAL)
            
        Returns:
            Dictionary with chunks, metadatas, similarities, and top_similarity
        """
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results or not results["documents"][0]:
                logger.info(f"No results for query: {query}")
                return {
                    "chunks": [],
                    "metadatas": [],
                    "similarities": [],
                    "top_similarity": 0.0
                }
            
            # Convert ChromaDB distances to cosine similarity scores
            # ChromaDB uses: distance = sqrt(2 * (1 - cosine_similarity))
            # So: cosine_similarity = 1 - (distance^2 / 2)
            # For small distances: similarity ≈ 1 - (distance / 2) works as approximation
            
            distances = results["distances"][0]
            similarities = [1 - (d / 2) for d in distances]  # Convert to similarity scores
            
            logger.info(f"Query retrieved {len(similarities)} results, top similarity: {similarities[0]:.3f}")
            
            return {
                "chunks": results["documents"][0],
                "metadatas": results["metadatas"][0],
                "similarities": similarities,
                "top_similarity": similarities[0] if similarities else 0.0
            }
        
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {
                "chunks": [],
                "metadatas": [],
                "similarities": [],
                "top_similarity": 0.0
            }
    
    def get_corpus_size(self) -> int:
        """Get total number of documents in corpus"""
        try:
            count = self.collection.count()
            return count
        except Exception as e:
            logger.error(f"Failed to get corpus size: {e}")
            return 0
    
    def delete_source(self, source: str) -> int:
        """
        Delete all chunks from a specific source.
        
        Args:
            source: Source filename/identifier
            
        Returns:
            Count of deleted chunks (approximate)
        """
        try:
            # Count before deletion
            count_before = self.collection.count()
            
            self.collection.delete(
                where={"source": source}
            )
            
            count_after = self.collection.count()
            deleted = count_before - count_after
            
            logger.info(f"Deleted {deleted} chunks from {source}")
            return deleted
        
        except Exception as e:
            logger.error(f"Failed to delete source {source}: {e}")
            return 0
    
    def get_all_sources(self) -> List[Dict[str, Any]]:
        """
        Get list of all unique sources (files) in corpus with metadata.
        
        Returns:
            List of dicts with source, file_type, chunk_count, and upload_date
        """
        try:
            # Get all documents
            all_docs = self.collection.get(include=["metadatas"])
            
            if not all_docs or not all_docs["metadatas"]:
                return []
            
            # Group by source
            sources_dict = {}
            for metadata in all_docs["metadatas"]:
                source = metadata.get("source", "unknown")
                if source not in sources_dict:
                    sources_dict[source] = {
                        "filename": source,
                        "file_type": metadata.get("type", "unknown"),
                        "chunk_count": 0,
                        "upload_date": metadata.get("timestamp", "")
                    }
                sources_dict[source]["chunk_count"] += 1
            
            result = list(sources_dict.values())
            logger.info(f"Found {len(result)} unique sources in corpus")
            return result
        
        except Exception as e:
            logger.error(f"Failed to get all sources: {e}")
            return []
    
    def has_single_pdf(self) -> bool:
        """
        Check if corpus contains exactly one file and it is a PDF.
        Used to auto-enable full-document mode for single PDF analysis.
        
        Returns:
            True if exactly one PDF file exists in corpus, False otherwise
        """
        try:
            sources = self.get_all_sources()
            if len(sources) == 1 and sources[0].get("file_type") == "pdf":
                logger.info("Single PDF detected - full-document mode can be auto-enabled")
                return True
            return False
        except Exception as e:
            logger.error(f"Error checking for single PDF: {e}")
            return False

    def get_all_documents(self) -> Dict[str, List[Any]]:
        """
        Get every stored chunk and its metadata for full-document synthesis.

        Returns:
            Dictionary with ordered chunks and metadatas lists
        """
        try:
            all_docs = self.collection.get(include=["documents", "metadatas"])

            if not all_docs or not all_docs.get("documents"):
                return {"chunks": [], "metadatas": []}

            combined = list(zip(all_docs.get("documents", []), all_docs.get("metadatas", [])))
            combined.sort(key=lambda item: (
                item[1].get("source", ""),
                item[1].get("chunk_index", 0)
            ))

            return {
                "chunks": [chunk for chunk, _ in combined],
                "metadatas": [meta for _, meta in combined],
            }

        except Exception as e:
            logger.error(f"Failed to get all documents: {e}")
            return {"chunks": [], "metadatas": []}
    
    def clear_corpus(self) -> int:
        """
        Delete all documents from corpus.
        
        Returns:
            Count of deleted documents
        """
        try:
            count_before = self.collection.count()
            if count_before == 0:
                return 0

            # Chroma delete(where={}) can be backend-version sensitive;
            # deleting by ids is the most reliable clear strategy.
            all_rows = self.collection.get(include=[])
            ids = all_rows.get("ids", []) if all_rows else []

            if not ids:
                return 0

            batch_size = 500
            for i in range(0, len(ids), batch_size):
                self.collection.delete(ids=ids[i:i + batch_size])

            count_after = self.collection.count()
            deleted = count_before - count_after
            
            logger.info(f"Cleared entire corpus. Deleted {deleted} documents")
            return deleted
        
        except Exception as e:
            logger.error(f"Failed to clear corpus: {e}")
            return 0


# Singleton instance for application
chroma_service = ChromaDBService()

