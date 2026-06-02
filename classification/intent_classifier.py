import json
import logging
from typing import List
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)

ALLOWED_INTENTS = {
    "billing",
    "technical_issue",
    "feature_request",
    "integration",
    "account_management",
    "data_and_export",
    "general_inquiry"
}

class IntentResult(BaseModel):
    intent: str
    confidence: float

    @field_validator("intent")
    @classmethod
    def validate_intent(cls, v: str) -> str:
        if v not in ALLOWED_INTENTS:
            raise ValueError(f"Intent '{v}' is not one of the allowed intents: {ALLOWED_INTENTS}")
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("Confidence must be a float between 0.0 and 1.0")
        return v

class IntentClassifier:
    def __init__(self, model: str = None):
        self.model = model or settings.generation_model
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def classify(self, query: str) -> IntentResult:
        """
        Calls the OpenAI chat completion API with a carefully designed prompt
        The model must return a JSON response with intent and confidence (float 0–1)
        Must parse and validate the response; on parse failure, return IntentResult(intent="general_inquiry", confidence=0.0)
        The prompt must include all 7 intent labels with descriptions
        """
        if not query or not query.strip():
            return IntentResult(intent="general_inquiry", confidence=0.0)

        system_prompt = """You are an intent classification assistant for Nexora (a B2B project management platform).
Your task is to classify incoming customer support queries into exactly one of the following 7 intents:

1. billing: Questions about pricing, invoices, plans, refunds, subscriptions.
2. technical_issue: Bugs, errors, crashes, unexpected behavior, system downtime.
3. feature_request: Asking about new features, capabilities, product roadmaps, suggestions.
4. integration: Questions about third-party integrations (e.g., Slack, GitHub, Jira).
5. account_management: Login, passwords, permissions, team members, two-factor authentication (2FA).
6. data_and_export: Project data exports, CSV/JSON backups, data management, recovery.
7. general_inquiry: Anything that does not fit the categories above (e.g., greetings, general questions about the company).

You must respond with a JSON object containing two keys:
- "intent": the exact string label of the classified intent (must be one of the 7 listed above).
- "confidence": a float value between 0.0 and 1.0 representing your confidence in this classification.

Example output:
{
  "intent": "billing",
  "confidence": 0.95
}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            result_text = response.choices[0].message.content
            data = json.loads(result_text)
            
            # Extract and validate fields
            intent = data.get("intent")
            confidence = data.get("confidence")
            
            if intent not in ALLOWED_INTENTS:
                logger.warning(f"Model returned invalid intent '{intent}', defaulting to general_inquiry.")
                return IntentResult(intent="general_inquiry", confidence=0.0)
                
            try:
                confidence_float = float(confidence)
                confidence_float = max(0.0, min(1.0, confidence_float))
            except (ValueError, TypeError):
                confidence_float = 0.0

            return IntentResult(intent=intent, confidence=confidence_float)
            
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return IntentResult(intent="general_inquiry", confidence=0.0)

    def classify_batch(self, queries: List[str]) -> List[IntentResult]:
        """
        Classifies each query independently
        Returns results in the same order
        """
        return [self.classify(q) for q in queries]
