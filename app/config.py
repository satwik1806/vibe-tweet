from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str

    # LLM API Keys (optional - only needed for the provider you use)
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    # Default LLM provider
    default_llm_provider: Literal["claude", "openai"] = "claude"

    @property
    def sync_database_url(self) -> str:
        """Convert async URL to sync URL for Alembic migrations."""
        return self.database_url.replace("+asyncpg", "")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
