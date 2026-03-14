from __future__ import annotations

import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Ecotrack"
    jwt_secret: str = os.environ.get("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24
    sqlite_path: str = "nrpt.db"
    # Set DATABASE_URL for production (e.g. Postgres on Railway/Render). If unset, uses SQLite.
    database_url: str | None = os.environ.get("DATABASE_URL")


settings = Settings()

