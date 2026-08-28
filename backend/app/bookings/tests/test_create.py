"""POST /bookings against a package-local app (main.py is a P1 hub)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.db import SessionLocal
from app.core.errors import register_exception_handlers
from app.bookings.router import router
from app.db_wipe import owner_session, wipe_product_rows
from app.facilities.seed import ensure_nairobi_seed
from app.symptoms.seed import ensure_symptom_catalog

_AUTH = {"Authorization": "Bearer test-token"}

_app = FastAPI()
_app.include_router(router)
register_exception_handlers(_app)


def _wipe() -> None:
    wipe_product_rows()


def _seed() -> int:
    session = SessionLocal()
    try:
        ensure_nairobi_seed(session)
        ensure_symptom_catalog(session)
        session.commit()
        facility_id = session.execute(
            text("SELECT id FROM facilities WHERE kmhfr_code = 'SEED-NBO-KNH'")
        ).scalar_one()
        return int(facility_id)
    finally:
        session.close()


def test_patient_books_and_wait_increments(mock_firebase_uid):
    _wipe()
    facility_id = _seed()
    mock_firebase_uid("demo-patient")
    client = TestClient(_app)

    before = SessionLocal()
    try:
        wait_before = int(
            before.execute(
                text("SELECT wait_count FROM facilities WHERE id = :id"),
                {"id": facility_id},
            ).scalar_one()
        )
    finally:
        before.close()

    response = client.post(
        "/bookings",
        headers=_AUTH,
        json={"facility_id": facility_id, "symptom_ids": ["chest-pain"]},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "booked"
    assert body["red_flag_applied"] is True
    assert body["keph_min_applied"] == 4
    assert body["symptom_ids"] == ["chest-pain"]
    assert body["facility"]["kmhfr_code"] == "SEED-NBO-KNH"
    assert body["facility"]["wait_count_at_book"] == wait_before

    with owner_session() as after:
        wait_after = int(
            after.execute(
                text("SELECT wait_count FROM facilities WHERE id = :id"),
                {"id": facility_id},
            ).scalar_one()
        )
        kinds = after.execute(
            text("SELECT booking_kind::text FROM bookings WHERE id = :id"),
            {"id": body["id"]},
        ).scalar_one()
        instant = after.execute(
            text("SELECT 1 FROM booking_instant WHERE booking_id = :id"),
            {"id": body["id"]},
        ).scalar_one()
    assert wait_after == wait_before + 1
    assert kinds == "instant"
    assert instant == 1


def test_staff_cannot_book(mock_firebase_uid):
    _wipe()
    facility_id = _seed()
    mock_firebase_uid("demo-staff")
    client = TestClient(_app)
    response = client.post(
        "/bookings",
        headers=_AUTH,
        json={"facility_id": facility_id, "symptom_ids": ["fever"]},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "forbidden"


def test_unknown_symptom_422(mock_firebase_uid):
    _wipe()
    facility_id = _seed()
    mock_firebase_uid("demo-patient")
    client = TestClient(_app)
    response = client.post(
        "/bookings",
        headers=_AUTH,
        json={"facility_id": facility_id, "symptom_ids": ["not-a-real-slug"]},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "unknown_symptom"
