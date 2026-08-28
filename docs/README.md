# Documentation — CareFlow

| Area | Path | Purpose |
|------|------|---------|
| Agent workflows | [agent-and-subagent-workflow.md](./agent-and-subagent-workflow.md) | Subagents, waves, runner/fixer |
| Mode SOPs | [agent-sops/](./agent-sops/) | Ask, Agent, Plan, Debug |
| API reference | [api/](./api/) | Human + agent HTTP chapters *(when `api-docs` module enabled)* |
| Testing | [testing-reference.md](./testing-reference.md) | Commands, pyramid, triage |
| Research / ADRs | [research/](./research/) | Decision records (ADRs) |
| Market research | [../research/](../research/) | Two-tier research workflow (`big-picture/` + `ops/`) |
| Plan conventions | [plan-conventions.md](./plan-conventions.md) | Wave plans in `~/.cursor/plans/` |
| Directory READMEs | [directory-readme-practice.md](./directory-readme-practice.md) | Top-level folder docs; nested READMEs by request only |

## Adding docs

- **Runbooks / how-to** → `docs/` (this tree)
- **Architecture decisions** → `docs/research/` per [research/AGENTS.md](./research/AGENTS.md)
- **Competitive / vendor research** → `research/` per [research/AGENTS.md](../research/AGENTS.md)
- **Ephemeral plans** → `~/.cursor/plans/` (not committed)
- **Top-level directory blurbs** → `<dir>/README.md` per [directory-readme-practice.md](./directory-readme-practice.md)
