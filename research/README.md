# Research

Competitive, market, and platform research for the **CareFlow** product domain — **separate from** application code and from architecture decision records (`docs/research/`).

## Two tiers

| Tier | Path | Question it answers | Typical outputs |
|------|------|---------------------|-----------------|
| **Big picture** | [`big-picture/`](big-picture/) | What does the market look like? Who competes? Where is whitespace? | Market maps, UX audits, competitor matrices, executive summaries |
| **Operations** | [`ops/`](ops/) | What do we build with? How do we implement? What backlog changes follow? | Stack choices, vendor comparisons, architecture specs, audits, traceability to features |

**Rule of thumb:** if the deliverable names a framework, API vendor, or sprint scope, it belongs in **ops**. If it names competitors, personas, or market gaps without prescribing implementation, it belongs in **big picture**.

```
research/
├── README.md                 ← you are here
├── AGENTS.md                 ← agent workflow (read before research work)
├── decision-log.md           ← cross-project locked decisions & risks
├── big-picture/              ← market & competitive research
│   ├── README.md
│   └── INDEX.md
├── ops/                      ← tactical & implementation research
│   ├── README.md
│   └── INDEX.md
└── _scaffolding/             ← templates for new research projects
```

## For humans

1. **Orient** — read this file and the tier README ([big-picture](big-picture/README.md) or [ops](ops/README.md)).
2. **Find prior work** — check the tier [`INDEX.md`](big-picture/INDEX.md) and [`decision-log.md`](decision-log.md) before starting something new.
3. **Open a project** — each project has its own `README.md`, `INDEX.md` (when multi-file), and `deliverables/`.
4. **Do not read** `meta/research-prompt*.md` unless you are reproducing or auditing methodology — prompts are archival only ([`AGENTS.md`](AGENTS.md)).

## For agents

**Start at [`AGENTS.md`](AGENTS.md).** It defines:

- When to load big-picture vs ops context (context budget rules)
- How to review prior research via subagents without filling the parent context
- Required scaffolding (`meta/decision-log.md`, `meta/big-picture-brief.md` for ops)
- Grill-me integration during planning (surface locked decisions and inconsistencies)
- Prompt archival policy (`.cursorignore`; no default reads)

## Related repo paths

| Path | Role |
|------|------|
| [`docs/research/`](../docs/research/) | ADRs — *why* a direction was chosen for implementation |
| [`docs/agent-and-subagent-workflow.md`](../docs/agent-and-subagent-workflow.md) | Multi-agent orchestration |
| [`.cursor/skills/mailsink-research/SKILL.md`](../.cursor/skills/mailsink-research/SKILL.md) | Email/OTP during authenticated research (if enabled at init) |
| [`.cursor/skills/grill-me/SKILL.md`](../.cursor/skills/grill-me/SKILL.md) | Plan-mode decision stress-test |

## Evidence conventions

- Tags: `[Verified]` / `[Likely]` / `[Unverified]`
- External URLs: append to project `meta/sources-log.md`
- CSV + markdown tables for importable data

## Starting new research

1. Choose tier: `big-picture/{slug}/` or `ops/{slug}/`.
2. Copy structure from [`_scaffolding/`](_scaffolding/README.md).
3. Add the project to the tier `INDEX.md` and any cross-links in `decision-log.md`.
4. Archive the executed prompt to `meta/research-prompt.md` (never remove from `.cursorignore`).
