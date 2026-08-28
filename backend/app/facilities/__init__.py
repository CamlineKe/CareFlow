"""Nairobi facility seed and routine recommend (FR-PL-03 / FR-PL-04)."""

from app.facilities.router import router
from app.facilities.seed import ensure_nairobi_seed

__all__ = ["router", "ensure_nairobi_seed"]
