import pytest
from config import settings
from classification.intent_classifier import IntentClassifier, IntentResult
from generation.prompt_builder import PromptBuilder
from generation.response_generator import ResponseGenerator, GeneratedResponse
from retrieval.vector_store import RetrievedChunk

openai_or_nvidia = pytest.mark.skipif(
    settings.openai_api_key in ("your-openai-api-key-here", "your-nvidia-api-key-here")
    or not (settings.openai_api_key.startswith("sk-") or settings.openai_api_key.startswith("nvapi-")),
    reason="Requires a valid OpenAI or NVIDIA API key"
)

@openai_or_nvidia
def test_classify_billing_intent():
    classifier = IntentClassifier()
    res = classifier.classify("How do I upgrade my subscription plan?")
    assert res.intent == "billing"
    assert 0.0 <= res.confidence <= 1.0

@openai_or_nvidia
def test_classify_technical_intent():
    classifier = IntentClassifier()
    res = classifier.classify("The app keeps crashing when I open a project")
    assert res.intent == "technical_issue"
    assert 0.0 <= res.confidence <= 1.0

@openai_or_nvidia
def test_classify_confidence_range():
    classifier = IntentClassifier()
    res = classifier.classify("Hello there, how are you?")
    assert 0.0 <= res.confidence <= 1.0

def test_build_rag_prompt_structure():
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_doc_001_0",
            doc_id="doc_001",
            content="This is onboarding information.",
            score=0.9,
            retrieval_method="hybrid"
        )
    ]
    intent = IntentResult(intent="general_inquiry", confidence=0.8)
    messages = PromptBuilder.build_rag_prompt("Hello", chunks, intent)
    
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"

def test_prompt_contains_chunk_ids():
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_doc_001_0",
            doc_id="doc_001",
            content="This is onboarding information.",
            score=0.9,
            retrieval_method="hybrid"
        ),
        RetrievedChunk(
            chunk_id="chunk_doc_002_5",
            doc_id="doc_002",
            content="Permission controls explanation.",
            score=0.8,
            retrieval_method="hybrid"
        )
    ]
    intent = IntentResult(intent="general_inquiry", confidence=0.8)
    messages = PromptBuilder.build_rag_prompt("Hello", chunks, intent)
    user_msg_content = messages[1]["content"]
    
    assert "chunk_doc_001_0" in user_msg_content
    assert "chunk_doc_002_5" in user_msg_content

@openai_or_nvidia
def test_generate_response_fields():
    generator = ResponseGenerator(max_tokens=50)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Reply with exactly 'Hi there'."}
    ]
    res = generator.generate(messages)
    assert isinstance(res, GeneratedResponse)
    assert res.response_text.strip() != ""
    assert res.total_tokens > 0
    assert res.prompt_tokens > 0
    assert res.completion_tokens > 0
