# Big-picture research

Broad **market and competitive** research — no stack choices, no vendor selection, no sprint scope.

## Purpose

Answer questions like:

- Who are the competitors and how do they behave?
- What UX patterns are table stakes vs whitespace?
- What platforms or communities exist in a region?
- What risks or regulatory norms shape the market?

Big-picture work **informs** ops research and product backlog; it does **not** prescribe implementation.

## When to use this tier

| Use big-picture | Use ops instead |
|-----------------|-----------------|
| Desk ranking of portals or communities | Choosing payment or messaging vendors |
| Live UX walkthrough of competitor sites | CRM feature parity matrix for *our* build |
| Market gap / whitespace analysis | Production stack or API resource outline |
| Persona and JTBD from competitive evidence | Docker compose sketch, sprint scope |

## Directory structure

Each project is a self-contained folder:

```
big-picture/{project-slug}/
├── README.md              ← research question, scope, deliverable index
├── INDEX.md               ← file map, status, subagent roster (multi-file runs)
├── meta/
│   ├── methodology.md     ← inclusion rules, ranking weights, evidence bar
│   ├── sources-log.md     ← append-only URL log
│   ├── orchestration-plan.md   ← optional; multi-agent runs
│   ├── context-budget-log.md   ← optional; coordinator context tracking
│   └── decision-log.md    ← strategic conclusions locked by this project
└── deliverables/          ← reports, CSVs, audits (the facts agents should read)
```

Copy the skeleton from [`../_scaffolding/`](../_scaffolding/README.md) when starting a new project.

## Projects

See [`INDEX.md`](INDEX.md) for the full catalog, status, and one-line findings.

## Downstream links

Ops projects should cite big-picture sources in `meta/big-picture-brief.md` (not re-ingest full deliverables). Locked market conclusions belong in each project's `meta/decision-log.md` and the repo [`decision-log.md`](../decision-log.md).

## Agents

Read [`../AGENTS.md`](../AGENTS.md) § Big picture tier. Default reads: this file → tier `INDEX.md` → project `README.md` → `deliverables/executive-summary.md` or audit report. Do **not** read `meta/research-prompt*.md` unless explicitly asked.
