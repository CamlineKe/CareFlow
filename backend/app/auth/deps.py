"""FastAPI dependencies: Bearer token, current user, RLS GUCs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.auth.firebase as firebase_tokens
from app.auth.seed import ensure_demo_users
from app.core.db import get_db
from app.core.rls import set_rls_gucs


@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: int
    firebase_uid: str
    role: str
    facility_id: int | None
    ui_locale: str
    phone_e164: str


def _unauthorized(message: str = "Missing or invalid Firebase ID token.") -> HTTPException:
    return HTTPException(
        status_code=401,
        detail={"code": "unauthorized", "message": message},
    )


def _not_provisioned() -> HTTPException:
    return HTTPException(
        status_code=404,
        detail={
            "code": "user_not_provisioned",
            "message": "No CareFlow user is provisioned for this Firebase account.",
        },
    )


def get_bearer_token(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    if authorization is None:
        raise _unauthorized()
    scheme, _, param = authorization.partition(" ")
    token = param.strip()
    if scheme.lower() != "bearer" or not token:
        raise _unauthorized()
    return token


def _pg_str(value: object) -> str:
    inner = getattr(value, "value", value)
    return str(inner)


def get_current_user(
    token: Annotated[str, Depends(get_bearer_token)],
    session: Annotated[Session, Depends(get_db)],
) -> CurrentUser:
    """Verify Firebase ID token, seed demo rows, load ``users``, set RLS GUCs."""
    try:
        decoded = firebase_tokens.verify_id_token(token)
    except firebase_tokens.FirebaseAuthError as exc:
        raise _unauthorized() from exc

    uid = decoded.get("uid") or decoded.get("sub")
    if not isinstance(uid, str) or not uid.strip():
        raise _unauthorized()
    uid = uid.strip()

    ensure_demo_users(session)

    row = session.execute(
        text(
            """
            SELECT id, firebase_uid, role, facility_id, ui_locale, phone_e164
            FROM users
            WHERE firebase_uid = :uid
            """
        ),
        {"uid": uid},
    ).mappings().first()

    if row is None:
        raise _not_provisioned()

    facility_id = row["facility_id"]
    if facility_id is not None:
        facility_id = int(facility_id)

    user = CurrentUser(
        id=int(row["id"]),
        firebase_uid=str(row["firebase_uid"]),
        role=_pg_str(row["role"]),
        facility_id=facility_id,
        ui_locale=_pg_str(row["ui_locale"]),
        phone_e164=str(row["phone_e164"]),
    )
    set_rls_gucs(
        session,
        user_id=user.id,
        role=user.role,
        facility_id=user.facility_id,
    )
    return user
