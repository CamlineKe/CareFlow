# Team issues — P1–P5 and T

Source of truth if GitHub issues cannot be created. After push, prefer `gh issue create` from these bodies. Labels: `person-p1` … `person-t`, `wave-1` / `wave-2`.

Attach [user-journeys.md](user-journeys.md) in every agent session. Epic: [kenya-pretriage.md](kenya-pretriage.md). Spec: [product-spec.md](product-spec.md).

---

## P1 — Platform, auth, Docker, Render

**Title:** `[P1] Firebase auth, Docker/Render, shared API core`

**Owns:** `backend/Dockerfile`, `docker-compose.yml`, `backend/app/core/`, `backend/app/auth/`, Alembic, Render blueprint, CI, `.env.example`. Polish baseline Compose. `GET /me`.

**Does not touch:** triage rules, bookings, notes, notify, `frontend/app/patient/**`, `frontend/app/hospital/**` (manifest/next config only if PWA install breaks).

**Journeys:** unblocks J1–J6 (sign-in). Not responsible for symptom UI.

**Acceptance:** ID token verified; patient vs staff roles in DB; staff has `facility_id`; Compose + `/health` on Render-shaped Dockerfile; secrets not committed.

**Subagents:** Docker vs Firebase Admin vs migrations — disjoint files.

---

## P2 — Facilities, KMHFR, symptom catalog

**Title:** `[P2] KMHFR ingest, ranking, Kenya symptom catalog + pgvector`

**Owns:** `backend/app/facilities/`, `backend/app/symptoms/` (canonical symptoms, language synonyms, embeddings, map-utterance API). Wave 2: `backend/app/triage/`, `backend/app/bookings/`.

**Does not touch:** Esri as SoT, frontend, notes, notify/ElevenLabs/Pawa.

**Journeys:** J1 steps 4–6, J2, J7, J8 mapping.

**Acceptance:** Kenya-only facilities; recommend wait-then-distance; utterance in `en`/`sw`/synonym langs maps to `symptom_id` above a confidence floor; rules still pick KEPH.

Read [research/big-picture/kenya-pretriage-landscape/deliverables/datasource-scorecard.md](../research/big-picture/kenya-pretriage-landscape/deliverables/datasource-scorecard.md) and `symptom-ontology-scorecard.md` before ingest.

---

## P3 — Care-seeker PWA

**Title:** `[P3] Patient PWA: voice landing, speak symptoms, book`

**Owns:** `frontend/app/patient/**`, landing `/` voice-consent greeting (J8), Firebase client, API client for map-symptom + recommend + book. In-app speech via **`POST /voice/stt` and `/voice/tts`** (do not call ElevenLabs or Pawa from the browser).

**Does not touch:** `/hospital/**`, backend ranking, outbound **phone** calls (P5).

**Journeys:** J1, J2, J7, J8.

**Acceptance:** Landing greets and asks to activate voice **before** other chrome; no mic until consent; spoken symptom path books a facility; en + sw UI strings.

---

## P4 — Hospital desk PWA

**Title:** `[P4] Hospital PWA: wait count, mark met / no-show`

**Owns:** `backend/app/hospital/`, `frontend/app/hospital/**` except `notes/`.

**Does not touch:** triage rules, SMS send, notes OCR, `frontend/app/patient/**`.

**Journeys:** J4, J5; triggers J3 via status change (P5 sends SMS).

**Acceptance:** Staff see only their facility; update wait; mark met / did not come; wait count moves with booking lifecycle as per OpenAPI.

---

## P5 — Notes, SMS, ElevenLabs + Pawa voice

**Title:** `[P5] Notes + SMS + ElevenLabs calls with Pawa AI fallback`

**Owns:** `backend/app/notes/`, `backend/app/notify/`, `backend/app/voice/` (ElevenLabs first; **[Pawa AI](https://docs.pawa-ai.com/)** STT/TTS fallback), `frontend/app/hospital/notes/**`.

**Does not touch:** ranking, wait UI, patient landing (except shared `/voice` API).

**Journeys:** J1 SMS, J3, J6, J8 STT/TTS backend, J9.

**Acceptance:** Demo flag logs SMS/calls if keys missing; cascade documented (en/sw → ElevenLabs, Kenyan local langs or ElevenLabs error → Pawa); notes persist text + transcript + image URLs + OCR; patients cannot read notes. Fail closed to text + SMS, never block booking.

---

## T — Tester

**Title:** `[T] Test plan, fixtures, pytest + Playwright J1–J9`

**Owns:** `backend/tests/`, `frontend/e2e/`, fixtures, test plan. Symptom-ontology scorecard expansion; competitor matrix; research prompt archival.

**Does not touch:** production feature folders except tests.

**Journeys:** J1–J9 including voice-consent (no mic without yes) and reminder-call demo log.

**Acceptance:** `docs/testing-reference.md` command; smoke J1, J5, J8 consent, J2; J3 no-show; J9 logged not live-dialled in CI.
