import time
import json
import logging
from typing import List
from openai import OpenAI
from config import settings
from ingestion.chunker import Chunk

logger = logging.getLogger(__name__)

class EmbeddingError(Exception):
    """Custom exception raised when OpenAI embedding API calls fail."""
    pass

class Embedder:
    def __init__(self, model: str = None, batch_size: int = 100):
        """
        model: OpenAI model to use (default: text-embedding-3-small)
        batch_size: batch size for embedding texts (default: 100)
        """
        self.model = model or settings.embedding_model
        self.batch_size = batch_size
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def embed_text(self, text: str, input_type: str = "query") -> List[float]:
        """
        Calls OpenAI's embedding API for a single string.
        Returns a list of 1536 floats.
        Must raise EmbeddingError if API call fails after 3 retries with exponential backoff (1s, 2s, 4s).
        """
        retries = 3
        delay = 1.0
        for attempt in range(retries + 1):
            try:
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model,
                    extra_body={"input_type": input_type}
                )
                return response.data[0].embedding
            except Exception as e:
                logger.warning(f"Embedding failed (attempt {attempt + 1}/{retries + 1}): {e}")
                if attempt < retries:
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise EmbeddingError(f"Failed to generate embedding after {retries} retries: {e}")

    def embed_batch(self, texts: List[str], input_type: str = "passage") -> List[List[float]]:
        """
        Embeds a list of texts in batches of batch_size.
        Returns embeddings in the same order as inputs.
        """
        embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            
            # API call with retry for the batch
            retries = 3
            delay = 1.0
            batch_embeddings = None
            
            for attempt in range(retries + 1):
                try:
                    response = self.client.embeddings.create(
                        input=batch_texts,
                        model=self.model,
                        extra_body={"input_type": input_type}
                    )
                    batch_embeddings = [item.embedding for item in response.data]
                    break
                except Exception as e:
                    logger.warning(f"Batch embedding failed (attempt {attempt + 1}/{retries + 1}): {e}")
                    if attempt < retries:
                        time.sleep(delay)
                        delay *= 2
                    else:
                        raise EmbeddingError(f"Failed to generate batch embedding after {retries} retries: {e}")
                        
            if batch_embeddings:
                embeddings.extend(batch_embeddings)
                
        return embeddings

    def embed_and_store_chunks(self, chunks: List[Chunk], conn) -> int:
        """
        Embeds all chunk contents.
        Inserts chunks into intellisupport.chunks including the embedding vector.
        Returns count of successfully stored chunks.
        """
        if not chunks:
            return 0
            
        # Get content strings to embed
        contents = [chunk.content for chunk in chunks]
        embeddings = self.embed_batch(contents)
        
        stored_count = 0
        with conn.cursor() as cur:
            for chunk, embedding in zip(chunks, embeddings):
                # Convert embedding list to pgvector string format: '[x1,x2,...]'
                embedding_str = "[" + ",".join(map(str, embedding)) + "]"
                
                cur.execute(
                    """
                    INSERT INTO intellisupport.chunks (chunk_id, doc_id, content, chunk_index, token_count, embedding, metadata, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s::vector, %s, NOW())
                    ON CONFLICT (chunk_id)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        token_count = EXCLUDED.token_count,
                        embedding = EXCLUDED.embedding,
                        metadata = EXCLUDED.metadata;
                    """,
                    (
                        chunk.chunk_id,
                        chunk.doc_id,
                        chunk.content,
                        chunk.chunk_index,
                        chunk.token_count,
                        embedding_str,
                        json.dumps(chunk.metadata),
                    )
                )
                stored_count += cur.rowcount
            conn.commit()
            
        return stored_count
