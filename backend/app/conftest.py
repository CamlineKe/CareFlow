"""Shared P2 fixtures for ``app/*/tests``. Nested conftest may define fixtures.

Do not set ``pytest_plugins`` here (pytest 8). Keep module imports light so
stdlib tests (catalog, hash, ranking, triage rules) do not load FastAPI.
"""

from __future__ import annotations

from collections.abc import Callable, Generator

import pytest


@pytest.fixture
def mock_firebase_uid(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    """Patch verify_id_token at the definition site (app.auth.firebase)."""

    def _set(uid: str) -> None:
        monkeypatch.setattr(
            "app.auth.firebase.verify_id_token",
            lambda token: {"uid": uid},
        )

    return _set


@pytest.fixture
def client() -> Generator:
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_reset() -> None:
    from app.db_wipe import wipe_product_rows

    wipe_product_rows()
