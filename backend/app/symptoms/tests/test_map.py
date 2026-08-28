"""POST /symptoms/map against a package-local app (main.py is a P1 hub)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import SessionLocal
from app.core.errors import register_exception_handlers
from app.symptoms.router import router
from app.symptoms.seed import ensure_symptom_catalog, ensure_synonym_embeddings

_map_app = FastAPI()
_map_app.include_router(router)
register_exception_handlers(_map_app)


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


def test_map_exact_english_phrase_returns_chest_pain_and_red_flag():
    _wipe_symptoms()
    session = SessionLocal()
    try:
        ensure_symptom_catalog(session)
        ensure_synonym_embeddings(session)
        session.commit()
    finally:
        session.close()

    client = TestClient(_map_app)
    response = client.post(
        "/symptoms/map",
        json={"text": "chest pain", "lang": "en"},
    )
    assert response.status_code == 200
    payload = response.json()
    slugs = [row["symptom_id"] for row in payload["matches"]]
    assert "chest-pain" in slugs
    assert payload["red_flag"] is True
    assert payload["keph_min"] == 4
    chest = next(row for row in payload["matches"] if row["symptom_id"] == "chest-pain")
    assert chest["score"] >= 0.55


def test_map_unknown_utterance_returns_empty_matches():
    _wipe_symptoms()
    session = SessionLocal()
    try:
        ensure_symptom_catalog(session)
        ensure_synonym_embeddings(session)
        session.commit()
    finally:
        session.close()

    client = TestClient(_map_app)
    response = client.post(
        "/symptoms/map",
        json={"text": "xyzzy-not-a-symptom-qqq", "lang": "en"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["matches"] == []
    assert payload["keph_min"] is None
    assert payload["red_flag"] is False


def test_map_rejects_unknown_lang():
    client = TestClient(_map_app)
    response = client.post(
        "/symptoms/map",
        json={"text": "homa", "lang": "fr"},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
