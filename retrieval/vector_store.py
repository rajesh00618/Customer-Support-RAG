from typing import List
from pydantic import BaseModel
from config import settings

class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    content: str
    score: float           # similarity score (0.0 to 1.0)
    retrieval_method: str  # "vector", "bm25", or "hybrid"

class VectorStore:
    def __init__(self, conn):
        self.conn = conn

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[RetrievedChunk]:
        """
        Uses cosine similarity via pgvector's <=> operator.
        Queries intellisupport.chunks for the top_k most similar chunks.
        Returns a list of RetrievedChunk objects sorted by similarity descending.
        """
        if not query_embedding:
            return []

        # Format embedding list as '[0.1, 0.2, ...]'
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        results = []
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_id, doc_id, content, embedding <=> %s::vector AS distance
                FROM intellisupport.chunks
                ORDER BY distance ASC
                LIMIT %s;
                """,
                (embedding_str, top_k)
            )
            rows = cur.fetchall()
            for row in rows:
                chunk_id, doc_id, content, distance = row
                # Handle possible null distance or edge cases
                if distance is None:
                    similarity_score = 0.0
                else:
                    similarity_score = 1.0 - distance
                
                results.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        doc_id=doc_id,
                        content=content,
                        score=max(0.0, min(1.0, similarity_score)),  # Clamping to 0-1
                        retrieval_method="vector"
                    )
                )
        return results

    def similarity_search_with_threshold(
        self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.75
    ) -> List[RetrievedChunk]:
        """
        Same as similarity_search but filters out results where cosine similarity is below threshold.
        """
        all_results = self.similarity_search(query_embedding, top_k)
        return [chunk for chunk in all_results if chunk.score >= threshold]
