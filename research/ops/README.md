# Operations research

**Tactical and implementation** research — vendor selection, architecture, authenticated product audits, and backlog traceability.

## Purpose

Answer questions like:

- Which payment or messaging vendor for our market?
- What does a competitor product expose and what should we match?
- What is the unified platform architecture for launch?
- How do third-party APIs integrate?

Ops work **depends on** big-picture context but goes into specifics that engineers and PMs act on.

## When to use this tier

| Use ops | Use big-picture instead |
|---------|-------------------------|
| Vendor fee comparison | Portal UX table-stakes prevalence |
| API backend + data model + deployment sketch | Market desk ranking |
| Product module inventory with evidence | Competitor trust-badge copy audit |
| Feature traceability to launch scope | Community landscape map |

## Directory structure

```
ops/{project-slug}/
├── README.md
├── INDEX.md               ← when multi-file or multi-wave
├── meta/
│   ├── methodology.md
│   ├── sources-log.md
│   ├── orchestration-plan.md      ← multi-agent runs
│   ├── decision-log.md            ← required: locked stack/vendor/scope choices
│   ├── big-picture-brief.md       ← required: upstream market context (links only)
│   └── context-budget-log.md      ← optional
├── deliverables/          ← reports, specs, CSVs
├── by-module/             ← optional; e.g. product walkthrough slices
└── scripts/               ← optional; capture automation
```

Scaffold from [`../_scaffolding/`](../_scaffolding/README.md).

## Projects

See [`INDEX.md`](INDEX.md) for catalog and recommendations.

## Upstream context (do not skip silently)

Before **new** ops research or **planning** that changes stack/backlog:

1. Read [`../decision-log.md`](../decision-log.md) — cross-project locked decisions.
2. Read linked entries in [`../big-picture/INDEX.md`](../big-picture/INDEX.md) — summaries only unless the task is market-facing.
3. If planning: use grill-me ([`.cursor/skills/grill-me/SKILL.md`](../../.cursor/skills/grill-me/SKILL.md)) to stress-test against prior decisions; spawn a readonly subagent for inconsistency checks ([`../AGENTS.md`](../AGENTS.md) § Context management).

Pure ops execution (e.g. "implement webhook from existing spec") should **not** load full big-picture CSVs — use `meta/big-picture-brief.md` and `decision-log.md` one-liners.

## Agents

Read [`../AGENTS.md`](../AGENTS.md) § Operations tier. Implementation ADRs go to [`docs/research/`](../../docs/research/) after ops decisions are accepted.
