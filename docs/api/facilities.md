# Facilities (recommend)

Journey **J7** only: rank operational facilities for routine (non-red-flag) pretriage. This is **not** diagnosis, not booking, and not a live KMHFR sync.

## Domain context

`GET /facilities/recommend` returns facilities the care-seeker can consider after a KEPH floor is known. Ranking uses desk-typed `wait_count` then great-circle distance. **`wait_count` is a demo ranking input, not HMIS** (INV-16, X-08). It is not queue position.

**Base path:** `/facilities` (no `/v1`). This chapter documents **`GET /recommend` only**.

**Authentication:** optional. The route is public; a Bearer token is not read and does not change ranking.

| Method | Path | Auth | OpenAPI tag |
|--------|------|------|-------------|
| `GET` | `/facilities/recommend` | None (optional Bearer ignored) | `facilities` |

**Geography:** `lat` and `lng` must lie in the Kenya bounding box (lat −5.0–5.6, lng 33.5–42.2). Outside → **400** `location_out_of_range`.

**Identifiers:** `id` is an integer facility primary key; `kmhfr_code` is the registry / seed string.

**Query vs response casing:** query keys and JSON keys are both snake_case (`lat`, `lng`, `keph_min`, `wait_count`, `distance_m`).

**Seed:** if `facilities` is empty, the handler loads committed Nairobi rows from `backend/data/nairobi-facilities.json`. If any row already exists, seed is a no-op. This pass does **not** call live KMHFR.

**Side effects:** empty-table Nairobi seed insert only. No booking, wait increment, or cache invalidation.

**Not in this chapter:** bookings, symptoms/map, voice, hospital queue, wait `PATCH`, red-flag distance-only KEPH 4+ ranking.

See [conventions.md](conventions.md) and [pagination-sorting-and-query-keys.md](pagination-sorting-and-query-keys.md).

**Related surfaces** (other chapters):

| Route | Chapter |
|-------|---------|
| `GET /health` | [health.md](health.md) |
| `GET /me` | [me.md](me.md) |

## Shared types

### `FacilityRecommendItem`

| JSON key | Type | Notes |
|----------|------|-------|
| `id` | integer | Facility primary key. |
| `kmhfr_code` | string | Registry / seed code (seed examples use `SEED-NBO-…`). |
| `name` | string | Display name. |
| `keph_level` | integer | KEPH 2–6. Filtered by `keph_min`. |
| `lat` | number | WGS84. |
| `lng` | number | WGS84. |
| `county` | string | e.g. Nairobi. |
| `wait_count` | integer | Desk-typed demo ranking input. **Not HMIS. Not queue position.** |
| `distance_m` | number | Metres from the query point; rounded to one decimal. |

### `FacilityRecommendResponse`

| JSON key | Type | Notes |
|----------|------|-------|
| `facilities` | `FacilityRecommendItem[]` | Unpaginated. May be empty. |

No cursor or offset wrapper. Bare object with a `facilities` array — not a `data` + `pagination` envelope.

## `GET /facilities/recommend`

- **Purpose** — Rank operational facilities at or above a KEPH floor by shortest desk wait, then nearest, for a point inside Kenya (J7 routine recommend).
- **Path parameters** — None.
- **Query parameters**

| Key | Type | Required | Default | Purpose |
|-----|------|----------|---------|---------|
| `lat` | number | yes | — | Care-seeker latitude. |
| `lng` | number | yes | — | Care-seeker longitude. |
| `keph_min` | integer | no | `2` | Inclusive KEPH floor. Allowed **2–6**. |

Unknown query keys are **ignored**. `keph_min` outside 2–6 → **422** `validation_error`. Missing `lat`/`lng` → **422** `validation_error`.

- **Request body** — None.
- **Success response** — `200`:

```json
{
  "facilities": [
    {
      "id": 1,
      "kmhfr_code": "SEED-NBO-KNH",
      "name": "Kenyatta National Hospital",
      "keph_level": 5,
      "lat": -1.3008,
      "lng": 36.8074,
      "county": "Nairobi",
      "wait_count": 11,
      "distance_m": 1234.5
    }
  ]
}
```

(`id` and `distance_m` depend on the database and query point; other fields match the Nairobi seed row.)

- **Errors**

| HTTP | `error.code` | When |
|------|----------------|------|
| 400 | `location_out_of_range` | `lat`/`lng` outside Kenya bbox. Message: `lat and lng must be inside Kenya.` |
| 422 | `validation_error` | Missing/invalid query (including `keph_min` not in 2–6). |

- **Behaviour notes**
  - Filter: `operational` is true **and** `keph_level >= keph_min`.
  - Sort: `wait_count ASC`, then `earth_distance` ASC (Postgres `cube` / `earthdistance`).
  - Empty table → Nairobi seed insert, then the same query.
  - Non-operational rows are excluded even if they exist in seed.
  - Red-flag ranking (distance-only, KEPH 4+) is **not** implemented here.
- **Try it**

  | Field | Value |
  |-------|-------|
  | `operationId` | `recommendFacilities` |
  | Postman request | Recommend facilities |
  | Tag | `facilities` |

  Nairobi example (`lat=-1.2921`, `lng=36.8219`, `keph_min=2`):

  ```bash
  curl "http://localhost:8000/facilities/recommend?lat=-1.2921&lng=36.8219&keph_min=2"
  ```

## Stable error codes and messages

| Code / message | HTTP | When |
|----------------|------|------|
| `location_out_of_range` / lat and lng must be inside Kenya. | 400 | Point outside Kenya bbox. |
| `validation_error` / (Pydantic message) | 422 | Query schema failed. |

## Relationship to other domains

Does not create a booking. Hospital staff must not treat this list as “all facilities I can desk” — desk scope is `facility_id` from [me.md](me.md). Health ([health.md](health.md)) does not mean recommend will succeed (needs migrated + reachable Postgres).

## Suggested view → API mapping

| Surface | Call |
|---------|------|
| Care-seeker recommend list (J7) | `GET /facilities/recommend?lat=&lng=&keph_min=` |
| Hospital desk | **Do not** use this route to choose workplace; this facility only via `/me` |

## Frontend notes

- Always pass `lat` and `lng` from a Kenya point; handle 400 `location_out_of_range` as “outside coverage”.
- Show `wait_count` as a **demo wait**, never as HMIS or live queue length.
- Sort is server-side; do not re-sort unless product asks.
- Online-only: the service worker must not cache this response.
- Optional auth: do not require `/me` before recommend.

## Implementation status snapshot (backend)

| Area | Status |
|------|--------|
| `GET /facilities/recommend` (J7) | **Implemented** |
| Live KMHFR sync | **Not implemented** (seed only; no SoT decision-log row this pass) |
| Red-flag recommend | **Not implemented** |
| Bookings / wait PATCH / queue | **Not implemented** (out of this chapter) |

## Reference files

- Route: `backend/app/facilities/router.py`
- Seed: `backend/app/facilities/seed.py`, `backend/data/nairobi-facilities.json`
- App include: `backend/app/main.py`
- Errors: `backend/app/core/errors.py`
- OpenAPI: `backend/openapi/openapi.yaml` (`operationId` `recommendFacilities`, tag `facilities`)
- Tests: `backend/tests/test_recommend.py`
