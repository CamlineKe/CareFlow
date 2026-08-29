"""Package-local notes fixtures with guarded owner setup and cleanup."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Generator, Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.core.config import normalize_database_url  # noqa: E402
from app.core.errors import register_exception_handlers  # noqa: E402
from app.notes.router import router as notes_router  # noqa: E402

_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "db"})
_LOCAL_OWNER = "postgresql://careflow_owner:careflow_owner@localhost:5432/careflow"
_RUN_ID = uuid4().hex[:12]
_FACILITY_CODE_PREFIX = f"NOTES-TEST-{_RUN_ID}-"
_USER_UID_PREFIX = f"notes-test-{_RUN_ID}-"
_SYMPTOM_SLUG = f"notes-test-{_RUN_ID}-symptom"
_PHONE_BASE = int(_RUN_ID[:8], 16) % 99_999_997


def _test_phone(offset: int) -> str:
    return f"+2547{(_PHONE_BASE + offset) % 100_000_000:08d}"


@dataclass(frozen=True, slots=True)
class NotesTestData:
    same_facility_booking_id: int
    other_facility_booking_id: int
    patient_uid: str
    same_facility_staff_uid: str
    other_facility_staff_uid: str


def _guarded_owner_url() -> str:
    app_raw = os.environ.get("DATABASE_URL", "")
    if not app_raw:
        raise RuntimeError("notes integration tests require DATABASE_URL")
    app_url = make_url(normalize_database_url(app_raw))
    if (
        app_url.host not in _LOCAL_HOSTS
        or app_url.database != "careflow"
        or app_url.username != "careflow"
    ):
        raise RuntimeError(
            "notes tests require the local CareFlow app-role database URL"
        )

    owner_raw = os.environ.get("DATABASE_ADMIN_URL") or _LOCAL_OWNER
    owner_url = normalize_database_url(owner_raw)
    parsed_owner = make_url(owner_url)
    if (
        parsed_owner.host not in _LOCAL_HOSTS
        or parsed_owner.database != "careflow"
        or parsed_owner.username != "careflow_owner"
    ):
        raise RuntimeError(
            "notes tests require the local CareFlow owner URL for guarded setup"
        )
    return owner_url


@contextmanager
def _owner_session() -> Iterator[Session]:
    engine = create_engine(_guarded_owner_url(), pool_pre_ping=True)
    factory = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


def _cleanup_notes_test_data(session: Session) -> None:
    booking_ids = list(
        session.execute(
            text(
                """
                SELECT b.id
                FROM bookings b
                JOIN facilities f ON f.id = b.facility_id
                WHERE f.kmhfr_code LIKE :facility_prefix
                """
            ),
            {"facility_prefix": f"{_FACILITY_CODE_PREFIX}%"},
        ).scalars()
    )
    for booking_id in booking_ids:
        params = {"booking_id": booking_id}
        session.execute(
            text(
                """
                DELETE FROM note_images
                WHERE note_id IN (
                    SELECT id FROM notes WHERE booking_id = :booking_id
                )
                """
            ),
            params,
        )
        session.execute(
            text("DELETE FROM notes WHERE booking_id = :booking_id"), params
        )
        session.execute(
            text("DELETE FROM notify_jobs WHERE booking_id = :booking_id"), params
        )
        session.execute(
            text(
                "DELETE FROM booking_facility_snapshots "
                "WHERE booking_id = :booking_id"
            ),
            params,
        )
        session.execute(
            text("DELETE FROM booking_symptoms WHERE booking_id = :booking_id"),
            params,
        )
        session.execute(
            text("DELETE FROM booking_instant WHERE booking_id = :booking_id"),
            params,
        )
        session.execute(
            text(
                "DELETE FROM booking_appointments WHERE booking_id = :booking_id"
            ),
            params,
        )
        session.execute(
            text("DELETE FROM bookings WHERE id = :booking_id"), params
        )
    session.execute(
        text("DELETE FROM users WHERE firebase_uid LIKE :uid_prefix"),
        {"uid_prefix": f"{_USER_UID_PREFIX}%"},
    )
    session.execute(
        text("DELETE FROM symptoms WHERE slug = :slug"),
        {"slug": _SYMPTOM_SLUG},
    )
    session.execute(
        text("DELETE FROM facilities WHERE kmhfr_code LIKE :facility_prefix"),
        {"facility_prefix": f"{_FACILITY_CODE_PREFIX}%"},
    )


def _insert_booking(
    session: Session, *, facility_id: int, patient_id: int, symptom_id: int
) -> int:
    booking_id = session.execute(
        text(
            """
            INSERT INTO bookings (
                facility_id, patient_user_id, booking_kind, booking_channel,
                status, notify_locale, keph_min_applied, red_flag_applied
            )
            VALUES (
                :facility_id, :patient_id,
                'instant', 'ranked_recommend',
                'booked', 'en', 3, false
            )
            RETURNING id
            """
        ),
        {"facility_id": facility_id, "patient_id": patient_id},
    ).scalar_one()
    session.execute(
        text("INSERT INTO booking_instant (booking_id) VALUES (:booking_id)"),
        {"booking_id": booking_id},
    )
    session.execute(
        text(
            """
            INSERT INTO booking_symptoms (
                booking_id, symptom_id, map_score, sort_order
            )
            VALUES (:booking_id, :symptom_id, 1.0, 0)
            """
        ),
        {"booking_id": booking_id, "symptom_id": symptom_id},
    )
    return int(booking_id)


@pytest.fixture(autouse=True)
def clean_notes_test_data() -> Generator[None, None, None]:
    with _owner_session() as session:
        _cleanup_notes_test_data(session)
    yield
    with _owner_session() as session:
        _cleanup_notes_test_data(session)


@pytest.fixture
def owner_session_factory() -> Callable[[], AbstractContextManager[Session]]:
    return _owner_session


@pytest.fixture
def notes_client() -> Generator[TestClient, None, None]:
    app = FastAPI()
    app.include_router(notes_router)
    register_exception_handlers(app)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_firebase_uid(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    def _set(uid: str) -> None:
        monkeypatch.setattr(
            "app.auth.firebase.verify_id_token",
            lambda _token: {"uid": uid},
        )

    return _set


@pytest.fixture
def notes_test_data() -> NotesTestData:
    patient_uid = f"{_USER_UID_PREFIX}patient"
    same_staff_uid = f"{_USER_UID_PREFIX}staff-same"
    other_staff_uid = f"{_USER_UID_PREFIX}staff-other"

    with _owner_session() as session:
        facility_ids: list[int] = []
        for suffix, name, lat in (
            ("SAME", "Notes Test Same Facility", -1.28),
            ("OTHER", "Notes Test Other Facility", -1.29),
        ):
            facility_id = session.execute(
                text(
                    """
                    INSERT INTO facilities (
                        kmhfr_code, name, keph_level, lat, lng, county,
                        operational, wait_count, source, synced_at
                    )
                    VALUES (
                        :code, :name, 3, :lat, 36.82, 'Nairobi',
                        true, 0, 'seed', now()
                    )
                    RETURNING id
                    """
                ),
                {
                    "code": f"{_FACILITY_CODE_PREFIX}{suffix}",
                    "name": name,
                    "lat": lat,
                },
            ).scalar_one()
            facility_ids.append(int(facility_id))

        patient_id = session.execute(
            text(
                """
                INSERT INTO users (
                    firebase_uid, role, facility_id, ui_locale, phone_e164
                )
                VALUES (:uid, 'patient', NULL, 'en', :phone)
                RETURNING id
                """
            ),
            {"uid": patient_uid, "phone": _test_phone(1)},
        ).scalar_one()
        for uid, facility_id, phone in (
            (same_staff_uid, facility_ids[0], _test_phone(2)),
            (other_staff_uid, facility_ids[1], _test_phone(3)),
        ):
            session.execute(
                text(
                    """
                    INSERT INTO users (
                        firebase_uid, role, facility_id, ui_locale, phone_e164
                    )
                    VALUES (
                        :uid, 'hospital_staff', :facility_id, 'en', :phone
                    )
                    """
                ),
                {"uid": uid, "facility_id": facility_id, "phone": phone},
            )

        symptom_id = session.execute(
            text(
                """
                INSERT INTO symptoms (slug, keph_min, red_flag, active)
                VALUES (:slug, 3, false, true)
                RETURNING id
                """
            ),
            {"slug": _SYMPTOM_SLUG},
        ).scalar_one()
        same_booking_id = _insert_booking(
            session,
            facility_id=facility_ids[0],
            patient_id=int(patient_id),
            symptom_id=int(symptom_id),
        )
        other_booking_id = _insert_booking(
            session,
            facility_id=facility_ids[1],
            patient_id=int(patient_id),
            symptom_id=int(symptom_id),
        )

    return NotesTestData(
        same_facility_booking_id=same_booking_id,
        other_facility_booking_id=other_booking_id,
        patient_uid=patient_uid,
        same_facility_staff_uid=same_staff_uid,
        other_facility_staff_uid=other_staff_uid,
    )
