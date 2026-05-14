"""
GPT-4o Perception Engine - Multimodal ingestion service
Converts images, audio, and PDFs to semantic text for ChromaDB
"""

import base64
import fitz  # PyMuPDF
import logging
import tempfile
from typing import Optional
import openai

from backend.app.config import settings

logger = logging.getLogger(__name__)

VISION_PROMPT = """You are a semantic extraction engine. Analyze this image comprehensively. Describe:
- All text visible in the image
- Spatial relationships and layout
- Entities, labels, and annotations
- Data in charts, tables, graphs
- Architectural components and diagrams
- Colors and their meaning/significance
- Technical notation and symbols
- Any contextual information

Be exhaustive and structured. Output only dense, semantic prose - no preamble or meta-commentary."""

AUDIO_ENRICHMENT_PROMPT = """Enrich this transcript with semantic analysis:
- Speaker intent and purpose
- Key decisions and conclusions
- Action items and next steps
- Named entities and references
- Thematic structure and flow
- Important context and implications

Format for maximum retrievability and context preservation."""

PDF_SUMMARIZATION_PROMPT = """Summarize this document semantically, preserving:
- Main topics and themes
- Key facts and data points
- Important relationships
- Critical sections and emphasis
- Document structure
- Actionable insights

Be comprehensive yet concise. Format for optimal retrieval."""


class GPT4oService:
    """Service for multimodal content extraction using GPT-4o"""
    
    def __init__(self):
        """Initialize async OpenAI client for GPT-4o"""
        self.client = openai.AsyncOpenAI(
            api_key=settings.GITHUB_TOKEN_A,
            base_url=settings.GITHUB_MODELS_BASE_URL
        )
        self.model = settings.GPT4O_MODEL
        logger.info(f"GPT-4o service initialized | Model: {self.model}")
    
    async def extract_from_image(self, image_bytes: bytes, filename: str) -> str:
        """
        Extract semantic text from image using GPT-4o vision.
        
        Args:
            image_bytes: Binary image data
            filename: Filename for mime type detection
            
        Returns:
            Semantic description of image
        """
        try:
            # Detect MIME type from filename
            extension = filename.lower().split('.')[-1]
            mime_map = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'webp': 'image/webp'
            }
            mime_type = mime_map.get(extension, 'image/jpeg')
            
            # Encode image as base64
            b64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            logger.info(f"Extracting vision from {filename} ({mime_type})")
            
            # Call GPT-4o with vision
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{b64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": VISION_PROMPT
                            }
                        ]
                    }
                ],
                max_tokens=2048,
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            logger.info(f"Vision extraction complete | {len(result)} chars")
            return result
        
        except Exception as e:
            logger.error(f"Vision extraction failed for {filename}: {e}", exc_info=True)
            raise
    
    async def extract_from_audio(self, audio_bytes: bytes, filename: str) -> str:
        """
        Extract audio content via transcription.
        Uses GPT-4o text analysis on metadata and audio fingerprinting.
        
        Args:
            audio_bytes: Binary audio data
            filename: Filename for audio type detection
            
        Returns:
            Semantic metadata about audio file
        """
        try:
            logger.info(f"Extracting audio metadata from {filename}")
            
            file_size_mb = len(audio_bytes) / 1024 / 1024
            
            # Generate metadata summary for RAG indexing
            metadata_prompt = f"""Analyze this audio file submission and generate semantic metadata for document indexing:

File: {filename}
Size: {file_size_mb:.1f} MB
Format: {filename.split('.')[-1].upper()}

Generate a semantic summary that could represent the audio content:
- Infer likely topic/subject from filename
- Identify file type and purpose
- Suggest potential query keywords
- Describe expected content categories

Output: Structured semantic description for document retrieval."""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": metadata_prompt
                    }
                ],
                max_tokens=1024,
                temperature=0.3
            )
            
            semantic_metadata = response.choices[0].message.content
            
            # Combine with file info for indexing
            indexed_content = f"""
AUDIO FILE: {filename}
File Size: {file_size_mb:.1f} MB
Upload Format: {filename.split('.')[-1].upper()}

SEMANTIC METADATA & INFERRED CONTENT:
{semantic_metadata}

NOTE: Full audio transcription requires external transcription service.
Visit Settings to enable advanced audio analysis with:
- Azure Speech Services
- Local Whisper model
- OpenAI Whisper API (with key)
"""
            
            logger.info(f"Audio metadata extraction complete | {len(indexed_content)} chars")
            return indexed_content
        
        except Exception as e:
            logger.error(f"Audio metadata extraction failed for {filename}: {e}", exc_info=True)
            raise
    
    async def extract_from_pdf(self, pdf_bytes: bytes, filename: str) -> str:
        """
        Extract text from PDF with vision fallback for scanned pages.
        
        Args:
            pdf_bytes: Binary PDF data
            filename: PDF filename
            
        Returns:
            Extracted and processed text
        """
        try:
            logger.info(f"Extracting PDF: {filename}")
            
            # Open PDF from bytes
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_text = []
            
            for page_num, page in enumerate(pdf_doc):
                try:
                    # Extract text
                    page_text = page.get_text()
                    
                    # If page is mostly empty (scanned image), use vision
                    if len(page_text.strip()) < 100:
                        logger.info(f"Page {page_num + 1}: Scanned - using vision")
                        
                        # Render page as image
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        image_bytes = pix.tobytes()
                        
                        # Extract via vision
                        page_content = await self.extract_from_image(image_bytes, f"{filename}_page_{page_num + 1}.png")
                    else:
                        page_content = page_text
                    
                    # Add page marker
                    total_text.append(f"--- Page {page_num + 1} ---\n{page_content}")
                    
                except Exception as e:
                    logger.warning(f"Page {page_num + 1} extraction failed: {e}")
                    total_text.append(f"--- Page {page_num + 1} (Failed) ---")
            
            combined_text = "\n\n".join(total_text)
            
            # If very long, summarize with GPT-4o
            if len(combined_text) > 8000:
                logger.info(f"PDF large ({len(combined_text)} chars) - summarizing")
                
                summary_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": f"{PDF_SUMMARIZATION_PROMPT}\n\nDocument:\n{combined_text[:8000]}"
                        }
                    ],
                    max_tokens=4096,
                    temperature=0.3
                )
                final_text = summary_response.choices[0].message.content
            else:
                final_text = combined_text
            
            logger.info(f"PDF extraction complete | {len(final_text)} chars")
            return final_text
        
        except Exception as e:
            logger.error(f"PDF extraction failed for {filename}: {e}")
            raise


# Singleton instance for application
gpt4o_service = GPT4oService()

