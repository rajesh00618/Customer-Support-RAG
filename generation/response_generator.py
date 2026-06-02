import logging
from pydantic import BaseModel
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)

class GeneratedResponse(BaseModel):
    response_text: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ResponseGenerator:
    def __init__(self, model: str = None, max_tokens: int = 512, temperature: float = 0.2):
        self.model = model or settings.generation_model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def generate(self, messages: list[dict]) -> GeneratedResponse:
        """
        Calls the OpenAI chat completion API
        Returns a GeneratedResponse object
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            response_text = response.choices[0].message.content or ""
            
            # Extract token usage safely
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0
            
            return GeneratedResponse(
                response_text=response_text,
                model=self.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            raise

    def generate_with_fallback(self, messages: list[dict], fallback_messages: list[dict]) -> GeneratedResponse:
        """
        Tries generate(messages) first
        If the response text is shorter than 20 characters or contains "I don't know" (case-insensitive),
        retries with fallback_messages.
        Returns whichever response has the longer response_text.
        """
        first_resp = self.generate(messages)
        first_text = first_resp.response_text.strip()
        
        # Check if first response fails criteria
        if len(first_text) < 20 or "i don't know" in first_text.lower():
            try:
                fallback_resp = self.generate(fallback_messages)
                # Compare lengths and return the longer response
                if len(fallback_resp.response_text.strip()) > len(first_text):
                    logger.info("Using fallback response because it is longer.")
                    return fallback_resp
            except Exception as e:
                logger.warning(f"Fallback generation failed, returning original response: {e}")
                
        return first_resp
