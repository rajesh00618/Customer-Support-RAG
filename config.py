from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    embedding_model: str = "text-embedding-3-small"
    generation_model: str = "gpt-4o-mini"
    openai_base_url: str = ""
    chunk_size: int = 512
    chunk_overlap: int = 50
    hybrid_alpha: float = 0.7
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_nvidia(self) -> bool:
        return "nvidia" in (self.openai_base_url or "").lower()


settings = Settings()
