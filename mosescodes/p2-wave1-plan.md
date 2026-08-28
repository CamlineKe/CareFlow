# P2 Wave 1 plan

| Field | Value |
|-------|-------|
| Document type | Implementation plan |
| Version | 0.1 |
| Status | Phase 1 complete; Phase 2 approved to start |
| Owner | Moses (P2) |
| Last updated | 2026-08-29 |
| Related documents | [p2-decisions.md](p2-decisions.md), [p2-task-map.md](p2-task-map.md), [p2-progress.md](p2-progress.md), [merge-clash-avoidance.md](../plans/merge-clash-avoidance.md) |
| Prerequisites | Decisions D-P2-01 … D-P2-07 |
| Revision summary | Phase 1 done; Phase 2 is the starter catalog |

## Goals and constraints

- Stay inside `backend/app/facilities/` and `backend/app/symptoms/` plus our API chapters.
- Do not edit hubs (`main.py`, `core/**`, `pyproject.toml`, Alembic, `docs/api/README.md`, `docs/api/conventions.md`).
- Do not edit `backend/tests/` or `frontend/`.
- Handshake P1 in writing before any hub change.
- After each phase: stop for approval.

## Phases

| Phase | Objective | Paths | Blocked by | Hub handshake |
|-------|-----------|-------|------------|---------------|
| **1. Red-flag ranking** | J2 on existing recommend | `facilities/`, `docs/api/facilities.md`, pagination row, OpenAPI export, Postman query key, `facilities/tests/` | None | None |
| **2. Symptom catalog JSON** | Starter catalog on disk | `backend/data/` + `symptoms/` loaders (no live route yet) | Phase 1 done | None yet |
| **3. Map API** | `POST /symptoms/map` package + chapter | `symptoms/` | Phase 2 | P1: `include_router`, README route-map row |
| **4. Real embeddings seed** | e5-small at seed time | seed job | Phase 3 | P1: pyproject extra, optional Settings |
| **5. KMHFR ingest** | Live sync | `facilities/` sync | Scorecards | P1: Settings / env name if token |

Phase 1 acceptance: `red_flag=false` keeps J7 wait-then-distance; `red_flag=true` drops KEPH &lt; 4 and sorts by distance only; Kangemi (Level 3) never appears on red-flag.

## Phase 1 detail

**Outcome:** `GET /facilities/recommend?red_flag=true` implements INV-07 on the Nairobi seed.

| File | Why | Change |
|------|-----|--------|
| `backend/app/facilities/ranking.py` | One place for the KEPH floor rule | `keph_floor(red_flag, keph_min)` |
| `backend/app/facilities/router.py` | Live route we own | New query; second SQL shape |
| `backend/app/facilities/tests/` | Feature tests, not T’s smoke tree | Red-flag vs routine order |
| `docs/api/facilities.md` | Domain chapter we own | Document `red_flag` |
| `docs/api/pagination-sorting-and-query-keys.md` | List contract for this route | Sort/filter note |
| `backend/openapi/openapi.yaml` | Must match live schema | Re-export |
| Postman facilities request | Optional query visible to P3 | `red_flag` |

**Does not change:** seed JSON, `main.py`, smoke tests in `backend/tests/test_recommend.py` (routine path must still pass).

**Verification:** pytest for `app/facilities/tests` plus existing `tests/test_recommend.py` if the backend venv and Compose `db` are up. Re-export OpenAPI with `python -m app.export_openapi` from that venv so committed YAML matches live schema (this pass patched YAML by hand because host Python has no FastAPI).
