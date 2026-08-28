# Current repo state

| Field | Value |
|-------|-------|
| Document type | Repo inventory |
| Version | 0.1 |
| Status | Draft |
| Owner | camline |
| Last updated | 2026-08-28 |
| Related documents | [01-problem.md](01-problem.md), [03-functional-requirements.md](03-functional-requirements.md) |
| Prerequisites | [01-problem.md](01-problem.md) |
| Revision summary | First inventory of specs vs empty app and research trees |

Previous: [01-problem.md](01-problem.md) · Next: [03-functional-requirements.md](03-functional-requirements.md)

## 1. One-line status

CareFlow is a **specified but unbuilt** hackathon product. Plans describe domain, journeys, APIs, and a stack. `backend/` and `frontend/` are empty placeholders. Research indexes and the decision log are empty. `[Verified]`

## 2. What exists

| Path | What it actually contains |
|------|---------------------------|
| [README.md](../README.md) | One-line product: Kenya pretriage PWA |
| [plans/kenya-pretriage.md](../plans/kenya-pretriage.md) | Feature plan, stack sketch, 6-person split, demo script. Marked locked for hackathon MVP |
| [plans/product-spec.md](../plans/product-spec.md) | Domain objects, PWA routes, API stubs, seed and env names |
| [plans/user-journeys.md](../plans/user-journeys.md) | J1–J9 actors and steps |
| [plans/team-issues.md](../plans/team-issues.md) | P1–P5 and T ownership |
| `backend/`, `frontend/` | README placeholders only. Stack "not chosen yet" |
| `research/` | Scaffolding only. Empty indexes, empty decision log |
| `docs/api/` | Generic API-doc stubs, no CareFlow routes |
| `.env.example` | Phantom template; `EXAMPLE_API_KEY` only |

## 3. Contradictions to resolve before design

These are not nits. They change what we are allowed to lock.

| Tension | Where | Why it matters |
|---------|-------|----------------|
| Stack is named in the plan (Next.js, FastAPI, PostgreSQL, pgvector, Firebase, Africa's Talking, ElevenLabs, Pawa, Twilio, Render) | [plans/kenya-pretriage.md](../plans/kenya-pretriage.md) | AGENTS.md, backend README, frontend README, and ONBOARDING still say **stack not chosen** |
| KMHFR is called the facility source of truth | Same plan | [research/decision-log.md](../research/decision-log.md) has **no rows**. The plan also says: no live KMHFR sync until a datasource scorecard exists **and** the decision log locks SoT |
| Cited research files do not exist | Plan links `research/big-picture/kenya-pretriage-landscape/deliverables/datasource-scorecard.md` and `symptom-ontology-scorecard.md` | Those paths are absent. Competitive and ontology claims are currently `[Unverified]` |
| API prefix | Product spec paths have no `/v1`; [docs/api/README.md](../docs/api/README.md) says all routes use `/v1` | Contract shape is unset |
| Six-person split vs this session | [plans/team-issues.md](../plans/team-issues.md) | Ownership assumes P1–P5 + T. Unclear if that team still exists |
| "Locked for hackathon MVP" vs empty decision log | Plan vs research | "Locked" in a plan is not the same as a recorded ADR or research decision |

## 4. Hard rule already in the plan

Do not build live `backend/app/facilities/` sync until:

1. The datasource scorecard exists, and
2. [research/decision-log.md](../research/decision-log.md) locks the source of truth

Until then, first boot recommends from committed seed / cache. `[Verified]`

That research has not been started in this repo. `[Verified]`

## 5. What "done" looks like in the plans (not yet our session goal)

The plan sequences:

- Wave 0: plans, journeys, issues, research scorecards, then Docker `/health`, PWA shells, seed recommend stub
- Wave 1: auth, KMHFR + catalog, patient/voice
- Wave 2: rules/bookings, book UI, hospital desk, notes/SMS/calls, tests
- Wave 3: Render + E2E for J1–J9

This camlinedev pass stops **before** Wave 0 implementation: problem + FRs + NFRs, then questions, then design.

## 6. Implications for requirements work

1. Treat the plans as a **candidate product definition**, not as a finished architecture.
2. Extract FRs and NFRs from journeys first. Stack, vendors, and module layout wait.
3. Anything that depends on missing research (KMHFR vs Esri, symptom ontologies, competitor whitespace) stays `[Unverified]` until we either do that research or you accept it as an assumption.
