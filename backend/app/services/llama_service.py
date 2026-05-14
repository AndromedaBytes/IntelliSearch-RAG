"""
Llama 3.1 405B Logic Engine - Reasoning and synthesis service
Uses 128k context window for cross-document synthesis and citation mapping
"""

import logging
from typing import List, Dict, Any
import openai

from backend.app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are IntelliSearch V2, a precise knowledge retrieval system.
You ONLY answer using the provided context chunks.

Rules:
- Base every claim on the retrieved context — never invent facts.
- When you use information from a source, you MUST cite it inline using [Source: filename] notation.
- If the context does not contain the answer, say exactly: "The information is not available in the ingested documents."
- Structure long answers with markdown headers and bullet points.
- Be concise but complete. Prioritize high-similarity chunks.
- If multiple sources contain relevant information, synthesize across them and cite each.
- Be transparent about confidence levels and gaps in context."""


class LlamaService:
    """Service for reasoning and synthesis using Llama 3.1 405B"""
    
    def __init__(self):
        """Initialize async OpenAI client for Llama 3.1 405B"""
        self.client = openai.AsyncOpenAI(
            api_key=settings.GITHUB_TOKEN_B,
            base_url=settings.GITHUB_MODELS_BASE_URL
        )
        self.model = settings.LLAMA_MODEL
        logger.info(f"Llama service initialized | Model: {self.model}")
    
    async def synthesize(
        self,
        query: str,
        context_chunks: List[str],
        metadatas: List[Dict[str, Any]]
    ) -> str:
        """
        Synthesize an answer from context chunks using Llama 3.1 405B.
        
        Args:
            query: User's query
            context_chunks: Retrieved context chunks from ChromaDB
            metadatas: Metadata for each chunk (source, type, etc)
            
        Returns:
            Synthesized answer with inline citations
        """
        # Build context string with minimal source headers (just filename)
        context_parts = []
        for i, (chunk, meta) in enumerate(zip(context_chunks, metadatas)):
            source = meta.get('source', 'unknown')
            
            context_parts.append(
                f"From {source}:\n{chunk}"
            )
        
        context_str = "\n\n".join(context_parts)
        
        # Build user prompt
        user_prompt = f"""Context from ingested documents:

{context_str}

Question: {query}"""
        
        logger.info(
            f"Synthesizing answer | Query length: {len(query)} | "
            f"Context chunks: {len(context_chunks)} | Total context: {len(context_str)} chars"
        )
        
        try:
            # Call Llama 3.1 405B
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4096,
                temperature=0.1  # Low temp for factual responses
            )
            
            answer = response.choices[0].message.content
            
            # Clean up any remaining source annotations that model may have included
            import re
            answer = re.sub(r'\s*\[Source:.*?\|.*?\|.*?\]\s*', '', answer, flags=re.DOTALL)
            
            logger.info(
                f"Synthesis complete | Response length: {len(answer)} chars | "
                f"Stop reason: {response.choices[0].finish_reason}"
            )
            
            return answer
        
        except Exception as e:
            logger.error(f"Synthesis failed for query '{query[:50]}...': {e}", exc_info=True)
            raise


# Singleton instance for application
llama_service = LlamaService()

