from typing import List
from pydantic import BaseModel, Field
from ingestion.loader import Document

class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    content: str
    chunk_index: int
    token_count: int
    metadata: dict = Field(default_factory=dict)

class DocumentChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        chunk_size: maximum number of tokens per chunk (not characters)
        chunk_overlap: number of overlapping tokens between consecutive chunks
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
            
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Document) -> List[Chunk]:
        """
        Splits document content into chunks respecting chunk_size and chunk_overlap.
        Each chunk receives a unique chunk_id generated as: f"chunk_{doc_id}_{chunk_index}"
        Sets chunk_index as the 0-based position.
        Estimates token_count using a simple whitespace tokenizer (split by spaces).
        """
        words = document.content.split()
        if not words:
            return []

        chunks = []
        chunk_index = 0
        step = self.chunk_size - self.chunk_overlap
        
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            content = " ".join(chunk_words)
            token_count = len(chunk_words)
            
            chunk_id = f"chunk_{document.doc_id}_{chunk_index}"
            
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=document.doc_id,
                    content=content,
                    chunk_index=chunk_index,
                    token_count=token_count,
                    metadata=document.metadata.copy()
                )
            )
            
            chunk_index += 1
            # If we reached the end of the document, break to avoid duplicating the last part
            if end >= len(words):
                break
                
            start += step
            
        return chunks

    def chunk_batch(self, documents: List[Document]) -> List[Chunk]:
        """
        Calls chunk_document for each document.
        Returns a flat list of all chunks.
        """
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks
