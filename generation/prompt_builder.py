from typing import List
from retrieval.vector_store import RetrievedChunk
from classification.intent_classifier import IntentResult

class PromptBuilder:
    @staticmethod
    def build_rag_prompt(query: str, retrieved_chunks: List[RetrievedChunk], intent: IntentResult) -> List[dict]:
        """
        Builds an OpenAI-format messages list: [{"role": "system", ...}, {"role": "user", ...}]
        System prompt:
          - Establishes assistant as "Nexora's AI Support Assistant"
          - Instructs the model to answer only from the provided context
          - Instructs the model to say "I don't have information about that" if context is insufficient
          - Includes the detected intent to guide tone
        User prompt:
          - Includes retrieved context chunks (numbered, with doc_id and chunk_id)
          - Includes customer's original query
          - Asks model to cite chunk_ids used in its response
        """
        system_content = (
            "You are Nexora's AI Support Assistant. Nexora is a B2B project management platform.\n"
            "Your task is to help users by answering their support queries using ONLY the provided context.\n\n"
            "Strict Guidelines:\n"
            "1. Ground your answers strictly in the provided context. Do not use any outside knowledge.\n"
            "2. If the context does not contain enough information to answer the query, you MUST say exactly: "
            "\"I don't have information about that\". Do not try to make up an answer.\n"
            "3. Do not make assumptions or extrapolate beyond the provided text.\n"
            f"4. The detected user intent for this query is: {intent.intent}. Use a polite and professional tone "
            "appropriate for this intent.\n"
        )
        
        context_str = ""
        for idx, chunk in enumerate(retrieved_chunks, 1):
            context_str += f"[{idx}] Chunk ID: {chunk.chunk_id} | Document ID: {chunk.doc_id}\nContent: {chunk.content}\n\n"
            
        user_content = (
            "Context Chunks:\n"
            f"{context_str}"
            f"Customer's Query: {query}\n\n"
            "Please construct a response to the customer's query. You MUST cite the specific Chunk IDs "
            "(e.g., [chunk_doc_001_0]) that you used to answer the question. If you do not have enough "
            "information in the chunks to answer, you must respond with: \"I don't have information about that\"."
        )
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def build_clarification_prompt(query: str, intent: IntentResult) -> List[dict]:
        """
        Used when no relevant chunks are retrieved (empty context).
        Builds a prompt asking the model to politely acknowledge the lack of information and ask a clarifying question.
        """
        system_content = (
            "You are Nexora's AI Support Assistant.\n"
            f"The user has asked a query under the intent '{intent.intent}'. However, no relevant information was found "
            "in Nexora's documentation to address this request.\n"
            "Politely acknowledge that you do not have information about this topic right now, and ask a helpful, "
            "specific clarifying question to assist them further."
        )
        
        user_content = f"Customer Query: {query}"
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def estimate_prompt_tokens(messages: List[dict]) -> int:
        """
        Estimates total token count of a messages list.
        Uses the formula: sum(len(m["content"].split()) * 1.3 for m in messages)
        Returns an integer.
        """
        token_sum = 0
        for m in messages:
            content = m.get("content", "")
            word_count = len(content.split())
            token_sum += word_count * 1.3
        return int(token_sum)
