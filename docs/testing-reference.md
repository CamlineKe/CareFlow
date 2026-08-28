# Testing reference — CareFlow

## Commands

| Layer | Command |
|-------|---------|
| Default (unit + integration) | `echo 'Set TEST_COMMAND in docs/testing-reference.md'` |
| Lint | `echo 'Set LINT_COMMAND in AGENTS.md'` |
| E2E / slow | <!-- e.g. npm run test:e2e --> |

## Pyramid

1. **Unit** — pure logic, mappers, utilities
2. **Integration** — API, DB, HTTP boundaries
3. **E2E** — critical user paths after unit/integration green

## Agent iteration

1. **Narrow** — smallest command that reproduces the failure
2. **Fix** — one layer (stub | app | assertion)
3. **Re-run narrow**
4. **Broaden** only when justified

See [agent-and-subagent-workflow.md](./agent-and-subagent-workflow.md) §6 (runner/fixer).

## Triage checklist

- [ ] Reproduces on CI or locally with documented env?
- [ ] Flaky vs deterministic?
- [ ] Wrong assertion vs wrong app behaviour vs missing stub?
- [ ] Shared types / API contract drift?
