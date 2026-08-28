# CareFlow — onboarding

Engineers setting up this repository for the first time. For production-oriented overview, see [README.md](README.md).

## Prerequisites

Stack is **not chosen yet**. Until then you only need:

- Git
- Node (for PDF scripts under `scripts/pdf/` and Phantom CLI)
- [Phantom](https://phm.dev) for secrets (see below)

Add language runtimes, Docker, and package managers when `backend/` / `frontend/` stacks are decided.

## First-time setup

```bash
cp .env.example .env
phantom init
# phantom add VAR_NAME   # when the first secret exists
```

Do not start an app yet — there is no runnable backend or frontend.

## Verify

Test and lint commands are placeholders until a stack is chosen. See [docs/testing-reference.md](docs/testing-reference.md).

## Directory map

| Directory | README | Topics |
|-----------|--------|--------|
| `backend/` | [backend/README.md](backend/README.md) | API and domain logic (stack TBD) |
| `frontend/` | [frontend/README.md](frontend/README.md) | User-facing app (stack TBD) |
| `docs/` | [docs/README.md](docs/README.md) | Agent SOPs, API reference stubs, testing |
| `plans/` | [plans/README.md](plans/README.md) | Committed specs, wave plan template |
| `camlinedev/` | [camlinedev/README.md](camlinedev/README.md) | Pre-design problem, draft FRs/NFRs, grill-me questions |
| `research/` | [research/README.md](research/README.md) | Market (`big-picture/`) and ops research |
| `scripts/` | [scripts/README.md](scripts/README.md) | PDF generation and other root scripts |

Add a row when you create a new top-level directory. Keep command details in linked READMEs — do not duplicate them here.

## Secrets (Phantom)

This project manages secrets with [Phantom](https://phm.dev) — API keys live in the OS keychain, not in `.env`.

**One-time machine setup:**

```bash
npm i -g phantom-secrets
npm i -g phantom-secrets-mcp
phantom init   # creates OS vault entry
```

**Add a secret** (replace `VAR_NAME` with the actual variable, e.g. `MAILSINK_API_KEY`):

```bash
phantom add VAR_NAME
# or via MCP: phantom_add_secret_interactive
```

**Variables used by this project:**

<!-- Fill in each secret this project uses, one per row -->
| Variable | Purpose |
|----------|---------|
| `EXAMPLE_API_KEY` | Replace with real variable name and purpose |

**MCP setup:** Merge `templates/cursor/mcp.phantom.json.snippet` into `.cursor/mcp.json` to enable the `phantom` MCP server in Cursor — this gives agents access to `phantom_add_secret_interactive` and `phantom_list_secrets` without exposing values in chat.

**`.env` file:** Contains phantom tokens (`phm_...`), not real secrets. Safe to commit if tracked; real values are injected by `phantom exec` at runtime.

## Related

- [README.md](README.md) — production-oriented overview
- [AGENTS.md](AGENTS.md) — agent baseline
- [docs/directory-readme-practice.md](docs/directory-readme-practice.md) — README conventions
