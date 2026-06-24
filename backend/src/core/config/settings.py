from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RAG SQL Chatbot"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    API_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://postgres:Shiva76619281@localhost:5432/rag_sql_chatbot"
    

    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"

    HUGGINGFACE_API_KEY: str | None = None



    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()