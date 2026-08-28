"""Owner-role DB helpers for P2 tests. Not used by request handlers.

Bookings have FORCE RLS and no DELETE policy, so the app role cannot wipe
them. Tests connect as the compose table owner (BYPASSRLS), same as Alembic.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import normalize_database_url

_COMPOSE_OWNER = "postgresql://careflow_owner:careflow_owner@localhost:5432/careflow"

_engine: Engine | None = None
_factory: sessionmaker[Session] | None = None

_WIPE_SQL = (
    "DELETE FROM note_images",
    "DELETE FROM notes",
    "DELETE FROM notify_jobs",
    "DELETE FROM booking_symptoms",
    "DELETE FROM booking_instant",
    "DELETE FROM booking_appointments",
    "DELETE FROM booking_facility_snapshots",
    "DELETE FROM bookings",
    "DELETE FROM user_preferred_facilities",
    "DELETE FROM patient_profiles",
    "DELETE FROM departments",
    "DELETE FROM users",
    "DELETE FROM facilities",
    "DELETE FROM symptom_synonyms",
    "DELETE FROM symptoms",
)


def _owner_engine() -> Engine:
    global _engine, _factory
    if _engine is None:
        raw = os.environ.get("DATABASE_ADMIN_URL") or _COMPOSE_OWNER
        _engine = create_engine(normalize_database_url(raw), pool_pre_ping=True)
        _factory = sessionmaker(
            bind=_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )
    return _engine


@contextmanager
def owner_session() -> Generator[Session, None, None]:
    _owner_engine()
    assert _factory is not None
    session = _factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def wipe_product_rows() -> None:
    """Delete pretriage rows as table owner so FORCE RLS does not hide them."""
    with owner_session() as session:
        for statement in _WIPE_SQL:
            session.execute(text(statement))
