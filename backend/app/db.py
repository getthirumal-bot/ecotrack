from __future__ import annotations

import logging
import os
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

if settings.database_url:
    # Production: Postgres (Railway/Render). Replace postgres:// with postgresql:// for SQLAlchemy.
    url = settings.database_url
    if url.startswith("postgres://"):
        url = "postgresql://" + url[10:]
    engine = create_engine(url, pool_pre_ping=True)
else:
    logging.warning(
        "Using SQLite. Data will not persist across container restarts/deploys. "
        "For production, set DATABASE_URL (e.g. Postgres)."
    )
    engine = create_engine(
        f"sqlite:///{settings.sqlite_path}",
        connect_args={"check_same_thread": False},
    )


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    if settings.database_url or os.environ.get("DATABASE_URL"):
        _run_postgres_migrations()
    else:
        _run_sqlite_migrations()


def _run_postgres_migrations() -> None:
    """Add columns to existing Postgres tables (create_all does not alter)."""
    try:
        with engine.begin() as conn:
            conn.execute(text(
                "ALTER TABLE project ADD COLUMN IF NOT EXISTS project_type VARCHAR DEFAULT 'implementation'"
            ))
    except Exception as e:
        logging.exception("Postgres migration failed: %s", e)
    # Verify column exists so startup fails fast if migration did not apply
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT project_type FROM project LIMIT 1"))
    except Exception as e:
        logging.warning("Project table missing project_type column or project table empty: %s", e)


def _run_sqlite_migrations() -> None:
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(defect)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "wbs_item_id" for row in rows):
                conn.execute(text("ALTER TABLE defect ADD COLUMN wbs_item_id VARCHAR"))
    except Exception:
        pass
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(defectattachment)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "phase" for row in rows):
                conn.execute(text("ALTER TABLE defectattachment ADD COLUMN phase VARCHAR DEFAULT 'before'"))
    except Exception:
        pass
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(boqitem)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "pending_approval" for row in rows):
                conn.execute(text("ALTER TABLE boqitem ADD COLUMN pending_approval BOOLEAN DEFAULT 0"))
    except Exception:
        pass
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(defect)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "display_number" for row in rows):
                conn.execute(text("ALTER TABLE defect ADD COLUMN display_number INTEGER"))
    except Exception:
        pass
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(materialmaster)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "pending_approval" for row in rows):
                conn.execute(text("ALTER TABLE materialmaster ADD COLUMN pending_approval BOOLEAN DEFAULT 0"))
    except Exception:
        pass
    # User extended fields and junction tables
    for col, default in [("phone", "''"), ("whatsapp_phone", "''"), ("address", "''")]:
        try:
            with engine.begin() as conn:
                r = conn.execute(text("PRAGMA table_info(user)"))
                rows = r.fetchall()
                if rows and not any(row[1] == col for row in rows):
                    conn.execute(text(f"ALTER TABLE user ADD COLUMN {col} VARCHAR DEFAULT {default}"))
        except Exception:
            pass
    # Project type (implementation | maintenance)
    try:
        with engine.begin() as conn:
            r = conn.execute(text("PRAGMA table_info(project)"))
            rows = r.fetchall()
            if rows and not any(row[1] == "project_type" for row in rows):
                conn.execute(text("ALTER TABLE project ADD COLUMN project_type VARCHAR DEFAULT 'implementation'"))
    except Exception:
        pass


def get_session():
    with Session(engine) as session:
        yield session

