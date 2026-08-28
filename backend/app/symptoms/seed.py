"""Insert canonical symptom rows when ``symptoms`` is empty.

Synonym embeddings are a later phase. This seed writes ``symptoms`` only.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.symptoms.catalog import Symptom, load_catalog

_INSERT = text(
    """
    INSERT INTO symptoms (
      slug, keph_min, red_flag, icd11_uri, ciel_concept_id, active
    ) VALUES (
      :slug, :keph_min, :red_flag, :icd11_uri, :ciel_concept_id, TRUE
    )
    """
)


def _row(symptom: Symptom) -> dict[str, object]:
    return {
        "slug": symptom.slug,
        "keph_min": symptom.keph_min,
        "red_flag": symptom.red_flag,
        "icd11_uri": symptom.icd11_uri,
        "ciel_concept_id": symptom.ciel_concept_id,
    }


def ensure_symptom_catalog(session: Session) -> None:
    """INSERT catalog rows when the table is empty. No-op if any row exists."""
    count = session.execute(text("SELECT COUNT(*) FROM symptoms")).scalar_one()
    if count > 0:
        return
    rows = [_row(item) for item in load_catalog()]
    if not rows:
        return
    session.execute(_INSERT, rows)
