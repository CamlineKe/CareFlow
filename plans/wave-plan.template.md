---
name: Feature name
overview: One-sentence goal for this epic
todos:
  - id: wave-0-discovery
    content: "Wave 0: readonly discovery subagents + decisions"
    status: pending
  - id: wave-1-foundation
    content: "Wave 1: parallel subagents — disjoint paths only"
    status: pending
  - id: wave-2-integration
    content: "Wave 2: parent merge + echo 'Set TEST_COMMAND in docs/testing-reference.md' + senior review (Ask)"
    status: pending
isProject: false
---

# Feature — subagent orchestration plan

## Goals and constraints

- **Parent** owns merge order, conflict resolution, `echo 'Set TEST_COMMAND in docs/testing-reference.md'`, and moving todos to done
- **Subagents** get bounded prompts: **owns**, **delivers**, **does not touch**
- **Disjoint ownership** — no two agents edit the same file in one wave

## Wave ownership

| Wave | Subagents | Owns (example) | Forbidden |
|------|-----------|----------------|-----------|
| 0 | explore (readonly) | — | writes |
| 1 | A, B parallel | `path/a/**`, `path/b/**` | each other's paths |
| 2 | parent | merge + tests | — |

## Flow

```mermaid
flowchart LR
  w0[Wave0 Discover]
  w1[Wave1 Parallel]
  gate[Test plus Review]
  w2[Wave2 Next]
  w0 --> w1 --> gate --> w2
```

## Acceptance criteria

- [ ] Each wave: disjoint paths documented
- [ ] Parent ran `echo 'Set TEST_COMMAND in docs/testing-reference.md'` between waves
- [ ] Senior review (Ask) before widening E2E scope
- [ ] No stack-specific rules duplicated here — use packs if needed
