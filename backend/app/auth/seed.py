"""Idempotent synthetic demo users (no public signup, no unknown-UID provision)."""

from sqlalchemy import text
from sqlalchemy.orm import Session

DEMO_PATIENT_UID = "demo-patient"
DEMO_STAFF_UID = "demo-staff"
DEMO_PATIENT_PHONE = "+254711111111"
DEMO_STAFF_PHONE = "+254722222222"
DEMO_STAFF_KMHFR = "SEED-NBO-KNH"
# Labeled local-demo login only (ONBOARDING). Never stored in Postgres.
DEMO_PATIENT_EMAIL = "patient@careflow.local"
DEMO_STAFF_EMAIL = "staff@careflow.local"
DEMO_PASSWORD = "CareflowDemo1!"


def ensure_demo_users(session: Session) -> None:
    """Insert demo care-seeker + hospital-staff rows if missing.

    Staff ``facility_id`` comes from ``facilities.kmhfr_code = SEED-NBO-KNH``
    (S-38: hospital staff without a facility is not a valid session).
    Unknown Firebase UIDs are never inserted.
    """
    from app.facilities.seed import ensure_nairobi_seed

    ensure_nairobi_seed(session)

    session.execute(
        text(
            """
            INSERT INTO users (firebase_uid, role, phone_e164, ui_locale, facility_id)
            VALUES (
                :uid,
                CAST(:role AS user_role),
                :phone,
                CAST(:locale AS ui_locale),
                NULL
            )
            ON CONFLICT (firebase_uid) DO NOTHING
            """
        ),
        {
            "uid": DEMO_PATIENT_UID,
            "role": "patient",
            "phone": DEMO_PATIENT_PHONE,
            "locale": "en",
        },
    )
    session.execute(
        text(
            """
            INSERT INTO users (firebase_uid, role, phone_e164, ui_locale, facility_id)
            SELECT
                :uid,
                CAST(:role AS user_role),
                :phone,
                CAST(:locale AS ui_locale),
                f.id
            FROM facilities f
            WHERE f.kmhfr_code = :kmhfr
            ON CONFLICT (firebase_uid) DO NOTHING
            """
        ),
        {
            "uid": DEMO_STAFF_UID,
            "role": "hospital_staff",
            "phone": DEMO_STAFF_PHONE,
            "locale": "en",
            "kmhfr": DEMO_STAFF_KMHFR,
        },
    )
