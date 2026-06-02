from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    openai_base_url: str = "https://integrate.api.nvidia.com/v1"
    database_url: str           # e.g., "postgresql://user:pass@localhost:5432/intellisupport"
    embedding_model: str = "nvidia/nv-embedqa-e5-v5"
    generation_model: str = "meta/llama-3.1-8b-instruct"
    chunk_size: int = 512
    chunk_overlap: int = 50
    hybrid_alpha: float = 0.7
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
