import time
import json
import logging
from typing import List
from openai import OpenAI
from config import settings
from ingestion.chunker import Chunk

logger = logging.getLogger(__name__)

class EmbeddingError(Exception):
    pass

class Embedder:
    def __init__(self, model: str = None, batch_size: int = 100):
        self.model = model or settings.embedding_model
        self.batch_size = batch_size
        base_url = settings.openai_base_url or None
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=base_url)
        self.is_nvidia = "nvidia" in (settings.openai_base_url or "").lower()

    def embed_text(self, text: str) -> List[float]:
        retries = 3
        delay = 1.0
        kwargs = {"input": text, "model": self.model}
        if self.is_nvidia:
            kwargs["extra_body"] = {"input_type": "query"}
        for attempt in range(retries + 1):
            try:
                response = self.client.embeddings.create(**kwargs)
                return response.data[0].embedding
            except Exception as e:
                logger.warning(f"Embedding failed (attempt {attempt + 1}/{retries + 1}): {e}")
                if attempt < retries:
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise EmbeddingError(f"Failed to generate embedding after {retries} retries: {e}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            retries = 3
            delay = 1.0
            batch_embeddings = None
            kwargs = {"input": batch_texts, "model": self.model}
            if self.is_nvidia:
                kwargs["extra_body"] = {"input_type": "passage"}
            for attempt in range(retries + 1):
                try:
                    response = self.client.embeddings.create(**kwargs)
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
        if not chunks:
            return 0
        contents = [chunk.content for chunk in chunks]
        embeddings = self.embed_batch(contents)
        stored_count = 0
        with conn.cursor() as cur:
            for chunk, embedding in zip(chunks, embeddings):
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
