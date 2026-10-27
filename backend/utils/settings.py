from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PGHOST: str = Field()
    PGPORT: int = Field(default=5432)
    PGUSER: str = Field()
    PGPASSWORD: str = Field()
    PGDATABASE: str = Field()

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    HTTP_TIMEOUT_SECONDS: float = Field(default=5)
    HTTP_MAX_RETRIES: int = Field(default=3)
    HTTP_RETRY_BACKOFF_SECONDS: float = Field(default=0.5)
    HTTP_RETRY_BACKOFF_MAX_SECONDS: float = Field(default=8)
    PROFOUND_API_BASE_URL: str = Field(default="https://profound.build")
    PROFOUND_API_BEARER_TOKEN: str = Field()

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
