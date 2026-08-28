# CareFlow — onboarding

Engineers setting up this repository for the first time. For production-oriented overview, see [README.md](README.md).

## Prerequisites

- Git
- [Docker](https://docs.docker.com/get-docker/) (Compose services `db` + `api`)
- Node 20 (PWA `frontend/` and Phantom CLI)
- Python 3.12 is **optional** on the host — Compose builds the FastAPI image
- [Phantom](https://phm.dev) for secrets (see below)

Locked stack: Next.js 15 PWA + FastAPI (Python 3.12) + PostgreSQL 16 + pgvector ([D-001](research/decision-log.md)).

## First-time setup

```bash
cp .env.example .env
phantom init
# phantom add FIREBASE_*   # needed for Auth user seed + ID tokens (see Local demo accounts)

docker compose up --build -d
# wait until db and api are healthy — api migrates then seeds on boot
curl localhost:8000/health   # {"status":"ok"}

cd frontend && npm install && npm run dev   # :3000
```

`docker compose up --build -d` is enough for migrate + seed. Do **not** run a separate `alembic upgrade head` on this first-time compose path. **Host pytest against `db` only** still needs Alembic on the host — see [docs/testing-reference.md](docs/testing-reference.md) (CI starts `db` only, then host Alembic + pytest).

After Compose is healthy, read [ARCHITECTURE.md](ARCHITECTURE.md) for target topology versus what is running now.

PWA: `/` role picker (no mic), `/patient` care-seeker + 999, `/hospital` desk this-facility-only. Manifest shortcuts `/patient` and `/hospital`. Service worker is online-only (does not cache API). There is **no PWA login UI this pass** (`frontend/app/page.tsx` is still a role picker).

`DEMO_NOTIFY=1` never live-dials. CORS allowlist is `FRONTEND_ORIGIN`. Env names: [`.env.example`](.env.example).

## Local demo accounts

**Local/demo only. Never use these credentials on a production Firebase project.**

| Email | Password | Role | Facility | Firebase UID |
|-------|----------|------|----------|--------------|
| `patient@careflow.local` | `CareflowDemo1!` | care-seeker (`patient`) | — | `demo-patient` |
| `staff@careflow.local` | `CareflowDemo1!` | hospital staff | Kenyatta National Hospital (`SEED-NBO-KNH`) | `demo-staff` |

PWA sign-in still needs `phantom add FIREBASE_*` so the boot seed can create Auth users and the client can obtain ID tokens. Pass those into Compose with `phantom exec -- docker compose up --build -d` (the `api` service interpolates `FIREBASE_*` from the host). These credentials are for operators, curl / `GET /me`, and a later Firebase client — not a login form this pass.

To re-seed without recreating the stack: `docker compose exec api python -m app.seed`.

## Verify

```bash
curl localhost:8000/health
cd backend && DEMO_NOTIFY=1 DATABASE_URL=postgresql://careflow:careflow@localhost:5432/careflow pytest
```

Host pytest talks to Compose `db` only. Full compose (`db` + `api`) migrates on boot; **db-only** (pytest / CI) still needs `alembic upgrade head` on the host. See [docs/testing-reference.md](docs/testing-reference.md).

Once `api` is up, Swagger UI is at [http://localhost:8000/docs](http://localhost:8000/docs). Committed OpenAPI: [backend/openapi/openapi.yaml](backend/openapi/openapi.yaml). Postman (repo JSON only): [docs/api/CareFlow.postman_collection.json](docs/api/CareFlow.postman_collection.json) and [docs/api/CareFlow.postman_environment.json](docs/api/CareFlow.postman_environment.json).

## Directory map

| Directory | README | Topics |
|-----------|--------|--------|
| `backend/` | [backend/README.md](backend/README.md) | FastAPI, Alembic, health / me / recommend |
| `frontend/` | [frontend/README.md](frontend/README.md) | Next.js 15 PWA shells |
| `docs/` | [docs/README.md](docs/README.md) | Agent SOPs, API reference, testing, [pre-design notes](docs/camlinedev.md) |
| `docs/product-map/` | [docs/product-map/README.md](docs/product-map/README.md) | Domain map: two sides, queue vs booking |
| `plans/` | [plans/README.md](plans/README.md) | Committed specs, wave plan template |
| `research/` | [research/README.md](research/README.md) | Market (`big-picture/`) and ops research |
| `scripts/` | [scripts/README.md](scripts/README.md) | PDF generation and other root scripts |

Add a row when you create a new top-level directory. Keep command details in linked READMEs — do not duplicate them here.

## Cursor plugins and MCP

Agent tooling for deploy and voice. No API keys in `mcp.json`. Both MCPs can create, change, or delete cloud resources — only grant access you are comfortable with.

**Render (plugin, user scope — all projects):**

1. In Cursor chat, run `/add-plugin render`.
2. Choose **user** scope, then **Authenticate** in the browser.
3. Verify: ask the agent to run `list_workspaces`.

Do **not** add a `render` entry to `.cursor/mcp.json` or `~/.cursor/mcp.json` — the plugin already provides the hosted MCP (`https://mcp.render.com/mcp`). If the plugin UI fails, add that URL in Customize → MCP with OAuth client id `cursor` instead.

**ElevenLabs (hosted MCP, OAuth):**

1. This repo already lists `elevenlabs` in [`.cursor/mcp.json`](.cursor/mcp.json) (`https://api.elevenlabs.io/v1/mcp`).
2. In **Customize → MCP**, click **Connect** / **Authenticate** for ElevenLabs and finish the browser OAuth. No API key.
3. If Cursor also loaded the same server from `~/.cursor/mcp.json`, disable one copy in Customize rather than deleting the repo file (teammates still need it).
4. App runtime keys (`ELEVENLABS_API_KEY`) stay in Phantom for later P5. If a skill asks you to write a key into `.env`, use `phantom add ELEVENLABS_API_KEY` instead and do not paste the key into chat.

**Phantom MCP:** [`.cursor/mcp.json`](.cursor/mcp.json) already includes the `phantom` stdio server. After Cursor reloads MCP, agents can use `phantom_add_secret_interactive` and `phantom_list_secrets` without exposing values in chat.

## Secrets (Phantom)

This project manages secrets with [Phantom](https://phm.dev) — API keys live in the OS keychain, not in `.env`.

**One-time machine setup:**

```bash
npm i -g phantom-secrets
npm i -g phantom-secrets-mcp
phantom init   # creates OS vault entry
```

**Add a secret** (replace `VAR_NAME` with the actual variable, e.g. `FIREBASE_PRIVATE_KEY`):

```bash
phantom add VAR_NAME
# or via MCP: phantom_add_secret_interactive
```

**Variables used by this project:** see [`.env.example`](.env.example). Names that matter locally:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | App-role Postgres (`careflow`). Compose sets this for `api`. |
| `DATABASE_ADMIN_URL` | Owner URL for Alembic (`careflow_owner`). |
| `FRONTEND_ORIGIN` | CORS allowlist for the PWA (default `http://localhost:3000`). |
| `NEXT_PUBLIC_API_URL` | PWA API base (default `http://localhost:8000`). |
| `DEMO_NOTIFY` | `1` = never live-dial or SMS-blast. Keep `1` unless you intend vendor traffic. |
| `FIREBASE_*` | Admin SDK for `GET /me` and boot seed (Phantom). Demo UIDs `demo-patient` / `demo-staff` (emails in [Local demo accounts](#local-demo-accounts)). |
| `ELEVENLABS_API_KEY` | App runtime for later TTS/STT/calls. **Not** required for hosted ElevenLabs MCP OAuth. |

**`.env` file:** Contains phantom tokens (`phm_...`), not real secrets. Safe to commit if tracked; real values are injected by `phantom exec` at runtime.

## Related

- [README.md](README.md) — production-oriented overview
- [ARCHITECTURE.md](ARCHITECTURE.md) — system topology (target vs as-built)
- [AGENTS.md](AGENTS.md) — agent baseline
- [docs/directory-readme-practice.md](docs/directory-readme-practice.md) — README conventions
