import logging
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from retrieval.vector_store import RetrievedChunk

logger = logging.getLogger(__name__)

class BM25Retriever:
    def __init__(self, conn):
        """
        On initialization, loads all chunks from intellisupport.chunks into memory
        Builds a BM25 index using the rank_bm25 library (BM25Okapi)
        Tokenizes chunk content by splitting on whitespace and lowercasing
        """
        self.chunks = []
        self.bm25 = None
        self.rebuild_index(conn)

    def rebuild_index(self, conn) -> None:
        """
        Reloads chunks from DB and rebuilds the BM25 index.
        Useful after new documents are ingested.
        """
        self.chunks = []
        tokenized_corpus = []
        
        with conn.cursor() as cur:
            cur.execute("SELECT chunk_id, doc_id, content FROM intellisupport.chunks;")
            rows = cur.fetchall()
            for row in rows:
                chunk_id, doc_id, content = row
                chunk_data = {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "content": content
                }
                self.chunks.append(chunk_data)
                # Tokenize content by lowercasing and splitting on whitespace
                tokenized_corpus.append(content.lower().split())
                
        if self.chunks:
            self.bm25 = BM25Okapi(tokenized_corpus)
        else:
            self.bm25 = None
            logger.warning("No chunks found in database. BM25 index is empty.")

    def search(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """
        Tokenizes the query the same way as during index building.
        Returns top_k results sorted by BM25 score descending.
        Normalizes BM25 scores to 0–1 range by dividing by the maximum score in the result set.
        If max score is 0, return an empty list.
        """
        if not self.bm25 or not self.chunks or not query:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        
        max_score = max(scores) if len(scores) > 0 else 0.0
        if max_score <= 0:
            return []

        # Zip chunks with their scores and normalize
        chunk_scores: List[Tuple[dict, float]] = []
        for chunk, score in zip(self.chunks, scores):
            normalized_score = score / max_score
            chunk_scores.append((chunk, normalized_score))

        # Sort by normalized score descending
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top_k
        top_results = chunk_scores[:top_k]
        
        # Convert to RetrievedChunk objects
        retrieved_chunks = []
        for chunk_data, score in top_results:
            # We filter out scores that are 0 or negative
            if score <= 0:
                continue
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_data["chunk_id"],
                    doc_id=chunk_data["doc_id"],
                    content=chunk_data["content"],
                    score=score,
                    retrieval_method="bm25"
                )
            )
            
        return retrieved_chunks
