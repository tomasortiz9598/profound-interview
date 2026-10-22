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
