# Agent guide: `docs/research/`

Authoring contract for agents creating or updating decision records under `docs/research/`.

## Required sections (decision record)

Use this order. Omit only when truly N/A (prefer `N/A` + one line).

### 1. Status

- **Outcome:** `Proposed` | `Draft` | `Accepted` | `Rejected` | `Superseded`
- **Date:** `YYYY-MM-DD`
- **Scope:** short phrase

### 2. Context

Problem, current behaviour, constraints. Write for a reader not in the original thread.

### 3. Options considered

One `### Option X: …` per alternative. Each option: **Flow** (numbered), **Pros**, **Cons**.

### 4. Decision

One clear line: `Choose **Option X**.` Plus implemented direction and explicit **non-goals**.

### 5. Why [option] was chosen

`## Why Option X Was Chosen` — bullets tied to **this codebase**, not generic platitudes.

### 6. Consequences

**Positive** and **Trade-offs** subsections.

### 7. Validation strategy (when applicable)

How the decision is proven: tests, migrations, manual steps. Skip only for early spikes — state what validation **will** be required.

### 8. Related files

Repo-relative paths. **Verify paths exist** before listing.

## Filename and title

- **Filename:** kebab-case (`member-transaction-mapping.md`)
- **H1:** short topic; include chosen option when decided

## Do not use this folder for

- API reference → `docs/api/`
- Runbooks → `docs/`
- Ephemeral plans → `~/.cursor/plans/`
