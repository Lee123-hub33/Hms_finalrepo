"""
Centralised settings loaded from the .env file.

pydantic-settings reads every field from environment variables automatically.
No credentials ever appear in source code.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Database ──────────────────────────────────────────────────────────────
    db_host:     str = "localhost"
    db_port:     int = 5432
    db_name:     str = "healthcare_db"
    db_user:     str = "postgres"
    db_password: str = "postgres"

    # ── Security ──────────────────────────────────────────────────────────────
    secret_key:                  str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 480
    algorithm:                   str = "HS256"

    # ── App ───────────────────────────────────────────────────────────────────
    app_env:         str  = "development"
    allowed_origins: str  = "http://localhost:8000"
    vite_api_url:    str  = ""

    @property
    def database_url(self) -> str:
        """Builds the connection string — password never hardcoded."""
        from urllib.parse import quote_plus
        pwd = quote_plus(self.db_password)
        return (
            f"postgresql://{self.db_user}:{pwd}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached singleton — only reads .env once per process.
    Use:  from app.config import get_settings; settings = get_settings()
    """
    return Settings()