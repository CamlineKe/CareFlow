# Handshake for P1 (Ethan) — symptoms map

| Field | Value |
|-------|-------|
| Document type | Hub handshake |
| Version | 0.1 |
| Status | Waiting on P1 |
| Owner | Moses (P2) |
| Last updated | 2026-08-29 |
| Related documents | [p2-wave1-plan.md](p2-wave1-plan.md), [merge-clash-avoidance.md](../plans/merge-clash-avoidance.md) |
| Prerequisites | Phase 3 package on `dev` |
| Revision summary | include_router for POST /symptoms/map |

P2 does not edit hub files. Please merge these one-liners so the route is live.

| File | One-line change | Why |
|------|-----------------|-----|
| `backend/app/main.py` | `from app.symptoms.router import router as symptoms_router` then `app.include_router(symptoms_router)` | J1 steps 4–6 and J8: P3 calls `POST /symptoms/map` then recommend |
| `docs/api/README.md` | Add route-map row `POST /symptoms/map` → [symptoms.md](../docs/api/symptoms.md) | Live routes must appear on the map after include |
| `backend/app/core/openapi.py` | Optional tag `{ "name": "symptoms", "description": "Utterance to catalog map" }` | Swagger grouping |

After include, from `backend/`: `python -m app.export_openapi` so `test_openapi.py` stays green (new path).

**Do not add** sentence-transformers yet. Wave 1 uses `careflow-hash-v1` vectors (exact phrase). Real e5-small is a later handshake (Phase 4).

**Auth:** route is public in Wave 1 (same as recommend). Patient Bearer can wait until bookings.
