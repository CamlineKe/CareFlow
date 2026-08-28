"""Insert canonical catalog rows when the symptoms table is empty."""

pytest_plugins = ["tests.conftest"]

from sqlalchemy import text

from app.core.db import SessionLocal
from app.symptoms.catalog import load_catalog
from app.symptoms.seed import ensure_symptom_catalog


def _wipe_symptoms() -> None:
    session = SessionLocal()
    try:
        session.execute(text("DELETE FROM booking_symptoms"))
        session.execute(text("DELETE FROM symptom_synonyms"))
        session.execute(text("DELETE FROM symptoms"))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def test_ensure_symptom_catalog_inserts_once():
    _wipe_symptoms()
    session = SessionLocal()
    try:
        ensure_symptom_catalog(session)
        session.commit()
        ensure_symptom_catalog(session)
        session.commit()
        count = session.execute(text("SELECT COUNT(*) FROM symptoms")).scalar_one()
        expected = len(load_catalog())
        assert count == expected
        chest = session.execute(
            text("SELECT red_flag, keph_min FROM symptoms WHERE slug = 'chest-pain'")
        ).one()
        assert chest.red_flag is True
        assert int(chest.keph_min) == 4
        synonym_count = session.execute(
            text("SELECT COUNT(*) FROM symptom_synonyms")
        ).scalar_one()
        assert synonym_count == 0
    finally:
        session.close()
