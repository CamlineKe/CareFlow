# Handshake for P1 (Ethan) — map and bookings

| Field | Value |
|-------|-------|
| Document type | Hub handshake |
| Version | 0.1 |
| Status | Waiting on P1 |
| Owner | Moses (P2) |
| Last updated | 2026-08-29 |
| Related documents | [p2-wave1-plan.md](p2-wave1-plan.md), [merge-clash-avoidance.md](../plans/merge-clash-avoidance.md) |
| Prerequisites | Phase 3 package on `dev` |
| Revision summary | include_router for map and bookings |

P2 does not edit hub files. Please merge these one-liners so the routes are live.

| File | One-line change | Why |
|------|-----------------|-----|
| `backend/app/main.py` | `include_router` for `app.symptoms.router` | J1/J8 `POST /symptoms/map` |
| `backend/app/main.py` | `include_router` for `app.bookings.router` | J1/J2 `POST /bookings` (wait **increment**) |
| `docs/api/README.md` | Route-map rows for `/symptoms/map` and `/bookings` | [symptoms.md](../docs/api/symptoms.md), [bookings.md](../docs/api/bookings.md) |
| `backend/app/core/openapi.py` | Optional tags `symptoms` and `bookings` | Swagger grouping |

After include, from `backend/`: `python -m app.export_openapi`.

**Do not add** sentence-transformers yet. Wave 1 map uses `careflow-hash-v1`.

**Auth:** map is public. Bookings require patient Bearer (`get_current_user`). Do not add `require_patient` unless you want it shared; P2 checks `user.role` in the bookings router.
