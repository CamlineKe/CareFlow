# Plan conventions

Large features use Cursor plans under `~/.cursor/plans/*.plan.md` (typically not committed).

## YAML frontmatter

```yaml
---
name: Short plan title
overview: One sentence goal
todos:
  - id: wave-1-slug
    content: "Wave 1: bounded deliverable"
    status: pending
isProject: false
---
```

## Body structure

1. **Goals and constraints** — parent vs subagent ownership
2. **Wave table** — id, scope, dependencies, disjoint paths
3. **Mermaid** (optional) — wave flow
4. **Acceptance criteria** — verifiable checklist

## Context budgets

| Role | Ceiling |
|------|---------|
| Plan-mode parent (orchestrating discovery) | ~85% — delegate wide reads to readonly subagents |
| Discovery subagent | ~90% — compact return only |
| Agent-mode parent (implementation waves) | ~85% when orchestrating |
| Implementation subagent | ~90% |

## Handoffs

| From | To | Deliverable |
|------|-----|-------------|
| **Plan** | **Agent** | Approved plan + wave todos + ownership table |
| **Ask** (review) | **Agent** | Prioritized fix list from senior review |
| **Agent** wave N | **Ask** | Senior review on merged diff before wave N+1 |

## Template

Copy [../plans/wave-plan.template.md](../plans/wave-plan.template.md) to `~/.cursor/plans/<feature>.plan.md` and rename waves.
