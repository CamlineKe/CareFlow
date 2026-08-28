# Research scaffolding templates

Copy this tree when starting a **new** research project. Replace `{tier}`, `{slug}`, and placeholders.

**Upstream template source:** [cursor-scaffold](~/Documents/Projects/cursor-scaffold) `templates/research/_scaffolding/` — sync generic changes there first, then backport to project-specific trees.

## Quick start

```bash
# Big picture
cp -R research/_scaffolding/project research/big-picture/{slug}

# Operations
cp -R research/_scaffolding/project research/ops/{slug}
```

Then:

1. Fill `README.md` and `meta/methodology.md`.
2. For **ops**: fill `meta/big-picture-brief.md` with links to upstream big-picture projects (no paste of full audits).
3. Add a row to the tier [`INDEX.md`](../big-picture/INDEX.md) or [`ops/INDEX.md`](../ops/INDEX.md).
4. Archive the executed prompt to `meta/research-prompt.md`.

## Template layout

```
_scaffolding/
├── README.md                 ← this file
└── project/                  ← copy this folder
    ├── README.md
    ├── INDEX.md
    ├── meta/
    │   ├── README.md
    │   ├── decision-log.md
    │   ├── big-picture-brief.md   ← ops only; delete for big-picture
    │   ├── methodology.md
    │   ├── sources-log.md
    │   ├── orchestration-plan.md  ← optional; multi-agent runs
    │   ├── context-budget-log.md ← optional; coordinator tracking
    │   └── research-prompt.header.md ← copy into research-prompt.md
    └── deliverables/
        └── README.md
```

## File purposes

| File | Description |
|------|-------------|
| `meta/decision-log.md` | Decisions **this project** locks; mirror key rows to [`../decision-log.md`](../decision-log.md) |
| `meta/big-picture-brief.md` | **Ops only** — upstream market context as links + short summary; keeps ops agents off full big-picture CSVs |
| `meta/methodology.md` | Inclusion rules, ranking weights, evidence bar |
| `meta/sources-log.md` | Append-only URL provenance |
| `meta/orchestration-plan.md` | Optional — multi-agent wave plan |
| `meta/context-budget-log.md` | Optional — coordinator context % notes |
| `INDEX.md` | Multi-file / multi-agent status tracker |

## Prompt archival

After the run, save the executed prompt to `meta/research-prompt.md` with the standard header from [`meta/research-prompt.header.md`](project/meta/research-prompt.header.md). Do not remove from `.cursorignore`. See [`../AGENTS.md`](../AGENTS.md).
