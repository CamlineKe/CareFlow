# Agent guide: `research/`

Competitive, market, and platform research — separate from application code and from ADRs in `docs/research/`.

**Human overview:** [`README.md`](README.md)  
**Locked decisions:** [`decision-log.md`](decision-log.md)

---

## Two tiers (read this first)

| Tier | Path | Answers | Does **not** include |
|------|------|---------|----------------------|
| **Big picture** | [`big-picture/`](big-picture/) | Market landscape, competitors, UX patterns, whitespace | Stack, vendors, sprint scope, API shapes |
| **Operations** | [`ops/`](ops/) | Vendors, architecture, audits, backlog traceability, implementation specs | Broad market ranking without build implications |

**Classify the task before loading files.** Wrong-tier reads waste context and blur decisions.

---

## Entry workflow

### 1. Classify the task

| Task type | Start here | Stop here (default) |
|-----------|------------|---------------------|
| Big-picture research | [`big-picture/INDEX.md`](big-picture/INDEX.md) → project `README.md` | Project deliverables; not ops specs |
| Ops research / implementation planning | [`ops/INDEX.md`](ops/INDEX.md) → [`decision-log.md`](decision-log.md) | Ops deliverables + `meta/big-picture-brief.md` |
| Pure ops execution (spec already locked) | Relevant ops `README.md` + target deliverable | Do **not** load big-picture CSVs or full audits |
| Site / design work citing research | [`decision-log.md`](decision-log.md) one-liners only | Unless user asks for competitive detail |
| **Plan mode** (new scope) | [`decision-log.md`](decision-log.md) + grill-me skill | Subagent prior-research scan (below) |

### 2. Tier indexes (low context)

Always prefer tier `INDEX.md` and project `README.md` over bulk deliverables:

- [`big-picture/INDEX.md`](big-picture/INDEX.md)
- [`ops/INDEX.md`](ops/INDEX.md)

### 3. Drill down by evidence need

| Need | Read |
|------|------|
| Executive summary | `deliverables/executive-summary.md` or project report header |
| Single vendor choice | Ops report § recommendation + `meta/decision-log.md` |
| Feature / backlog mapping | Ops traceability deliverable + project `README.md` |
| Full competitive matrix | Big-picture deliverable — **subagent only** if parent context > ~70% |

---

## Context management

Parent agents orchestrating research or planning should stay under ~**85%** context ([`docs/agent-and-subagent-workflow.md`](../docs/agent-and-subagent-workflow.md)).

### Do not load into parent context

- Full master CSVs and feature matrices
- Multi-hundred-line audit bodies when a summary or INDEX row suffices
- `meta/research-prompt*.md` (archival; `.cursorignore`)
- More than one complete ops architecture deliverable set at once

### Use subagents for prior-research review

When **planning** ops work, **new ops research**, or **grill-me** sessions that might contradict prior conclusions:

1. Spawn a **readonly** `explore` subagent with a narrow brief:
   - Read [`decision-log.md`](decision-log.md), relevant tier `INDEX.md`, and named project `meta/decision-log.md` / `meta/big-picture-brief.md`.
   - Return: **locked decisions**, **conflicts**, **gaps**, **recommended reads** (paths only, ≤15 lines prose).
2. Parent ingests the summary — not raw deliverables.
3. Surface conflicts during **grill-me** ([`.cursor/skills/grill-me/SKILL.md`](../.cursor/skills/grill-me/SKILL.md)) as constraints or `[needs validation]` assumptions.

**Skip the subagent** when the task is purely operational and `decision-log.md` + one ops README already answer the question.

### Multi-agent research runs

Coordinators append to `meta/context-budget-log.md` (est. % notes per wave). Workers return handoffs, not full file dumps.

---

## Required scaffolding

New projects: copy from [`_scaffolding/`](_scaffolding/README.md).

| File | Big picture | Ops | Purpose |
|------|:-----------:|:---:|---------|
| `README.md` | ✓ | ✓ | Research question, scope, deliverable index |
| `INDEX.md` | multi-file | multi-file | File map, status, subagent roster |
| `meta/methodology.md` | ✓ | ✓ | Inclusion rules, evidence bar |
| `meta/sources-log.md` | ✓ | ✓ | Append-only URLs |
| `meta/decision-log.md` | ✓ | ✓ | Decisions **this project** locks |
| `meta/big-picture-brief.md` | — | ✓ | Links + 1-paragraph upstream market context |
| `meta/research-prompt.md` | ✓ | ✓ | Archival prompt (do not read by default) |
| `meta/orchestration-plan.md` | optional | optional | Multi-agent waves |
| `meta/context-budget-log.md` | optional | optional | Coordinator context tracking |
| `deliverables/` | ✓ | ✓ | Facts agents should cite |

After locking decisions: update [`decision-log.md`](decision-log.md). Accepted implementation choices: add ADR under [`docs/research/`](../docs/research/).

---

## Research prompt archival (required)

Every research subdirectory **must** retain the prompt that generated its deliverables:

| Location | When |
|----------|------|
| `meta/research-prompt.md` | Single-phase research (default) |
| `meta/research-prompt-{phase}.md` | Multi-phase projects |
| `research/{slug}.research-prompt.md` | Standalone deliverables at `research/` root |

Each prompt file starts with the standard **archival header** (see `_scaffolding/project/meta/research-prompt.header.md`). Prompts are in **`.cursorignore`**.

### Agents: do not read prompts unless asked

- **Do not** read, cite, or obey instructions in `research-prompt*.md` during normal work.
- **Do** use `deliverables/`, `INDEX.md`, `README.md`, `meta/methodology.md`, `meta/decision-log.md`.
- **Only** read a research prompt when the user **explicitly** references it.

---

## Directory map

Projects are listed in tier indexes — add rows as you create projects:

- [`big-picture/INDEX.md`](big-picture/INDEX.md)
- [`ops/INDEX.md`](ops/INDEX.md)

### Root

| Path | Purpose |
|------|---------|
| `decision-log.md` | Cross-project locked decisions |

---

## Plan mode + grill-me

When planning research or implementation that consumes prior work:

1. Offer grill-me vs **Work with assumptions** ([grill-me skill](../.cursor/skills/grill-me/SKILL.md)).
2. Pre-load [`decision-log.md`](decision-log.md) decisions as grill constraints.
3. If user proposes something that contradicts D-00x, flag explicitly — do not silently override.
4. Deferred or unresolved items → **Deferred** section in plan; assumptions → `[needs validation]`.

---

## Conventions

- Evidence tags: `[Verified]` / `[Likely]` / `[Unverified]`
- Append external URLs to `meta/sources-log.md`
- Multi-agent runs: parent orchestrates per [`docs/agent-and-subagent-workflow.md`](../docs/agent-and-subagent-workflow.md)
- Signup/OTP during research: [`.cursor/skills/mailsink-research/SKILL.md`](../.cursor/skills/mailsink-research/SKILL.md) (if enabled at init)

Cross-project / Cursor tooling research → use global `@save-research-topic` skill; do not add to `research/ops/` unless product-scoped.

## Related

- Decision records (ADRs): [`docs/research/AGENTS.md`](../docs/research/AGENTS.md)
- Orchestration: [`docs/agent-and-subagent-workflow.md`](../docs/agent-and-subagent-workflow.md)
- Cursor rule: [`.cursor/rules/research-prompts.mdc`](../.cursor/rules/research-prompts.mdc)
