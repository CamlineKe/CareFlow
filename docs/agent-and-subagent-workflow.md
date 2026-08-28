# Agent and subagent workflow — CareFlow

**Binding for agents:** When the user, a plan, or repo instructions mention **building with subagents** (parallel **Task** subagents / multi-agent waves), read this file end-to-end before partitioning work.

**Exception (narrow):** If the **parent** can **complete the entire scoped task** in one thread and stay **under ~90%** context, it may implement in-thread without parallel Task subagents — still apply disjoint ownership, runner/fixer splits, and wave gates where relevant.

Stack: **generic**. Tests: **`echo 'Set TEST_COMMAND in docs/testing-reference.md'`**. Lint: **`echo 'Set LINT_COMMAND in AGENTS.md'`**.

---

## 1. Roles

**Parent session** owns merge order, conflict resolution, when to run tests, and whether a change set is approved.

**Subagents** own **bounded** work: each prompt lists **owns**, **delivers**, and **does not touch** paths. Return structured output (what changed, what to verify, risks).

---

## 2. When to use subagents

Use parallel subagents only when ownership is **disjoint** — no two agents edit the same file in the same wave.

**Good partitions**

- **By layer:** e.g. API client vs utilities vs one feature folder
- **By test stream:** one agent on fixtures/mocks, another on a single spec file

After phases that touch **shared types** or **API contracts**, run **`echo 'Set TEST_COMMAND in docs/testing-reference.md'`** on the integrated branch early.

---

## 3. Orchestration patterns

**Parent as orchestrator — ~85% ceiling:** When the parent mainly coordinates, treat **~85%** context as the practical ceiling. Heavy reads and logs stay in subagent threads; the parent receives **short handbacks**.

**Explicit handoff** in each subagent prompt:

- **Owns:** glob or path list
- **Delivers:** files, behaviour, or tests
- **Does not touch:** paths another agent owns

**Parent between waves:** merge → **`echo 'Set TEST_COMMAND in docs/testing-reference.md'`** → senior review (Ask) → next wave.

Wave breakdowns may live in `~/.cursor/plans/` (not committed).

---

## 4. Senior review loop

After a feature slice:

- Follow `.cursor/rules/senior-code-review.mdc` and `.claude/commands/senior-review.md`
- Triage **Critical** / **blockers** before design and nits
- Fix in **Agent** mode; re-review or spot-check until merge-ready

---

## 5. Ask mode for senior review

Run senior review in **Ask mode** (read-only). Keeps review and implementation diffs in separate threads.

Use **Agent mode** for applying fixes.

---

## 6. Runner / fixer split (slow tests)

### Runner (read-only)

- Run narrowed integration/E2E command from [testing-reference.md](./testing-reference.md)
- Capture: failing path, error text, trace/log location
- **Classify** failure: **stub** | **app** | **assertion**
- Output a **short structured report** — not a full-repo rewrite plan

### Fixer (write, scoped)

- Edit only the implicated layer per the runner report
- Do not assign “run full suite and refactor half the repo” to one agent

### Parent

Merge each fix → **runner → fixer → runner** until green. Parent decides when a full-suite gate is worth the cost.

---

## 7. Pointers

| Topic | Where |
|--------|--------|
| Repo baseline | [AGENTS.md](../AGENTS.md) |
| Mode playbooks | [agent-sops/](./agent-sops/) |
| Testing commands | [testing-reference.md](./testing-reference.md) |
| ADRs | [research/](./research/) |
| Plan waves | [plan-conventions.md](./plan-conventions.md) |
| Senior review rule | [.cursor/rules/senior-code-review.mdc](../.cursor/rules/senior-code-review.mdc) |
