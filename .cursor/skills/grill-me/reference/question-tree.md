# Grill-me question tree

Use this inventory to build a **silent** question queue. Filter aggressively — most sessions need 5–15 questions, not every branch.

Legend: **B** = blocking (ask early) · **E** = explore codebase first · **S** = skip if user chose Work with assumptions

---

## 1. Goal and success — B

- What problem are we solving? For whom?
- What does "done" look like — demo, ship, research artifact, doc?
- How will we know it worked (metric, test, review gate)?
- Is this new work, a fix, refactor, or research spike?
- What happens if we do nothing?

## 2. Scope and boundaries — B

- MVP vs full vision — what ships in this pass?
- Explicit **out of scope** list?
- Which directories/trees are touched (`eleventy/`, `research/`, `tests/`, docs only)?
- Reuse existing patterns vs greenfield?
- One PR or multi-wave / multi-PR delivery?

## 3. Constraints — B

- Hard deadline or sequencing dependencies?
- Must-not-break surfaces (SEO, production URLs, research deliverable format)?
- Budget for dependencies, APIs, or paid services?
- Compliance, licensing, or PII constraints?
- Team capacity — solo agent session vs human review gates?

## 4. Users and stakeholders — B

- Primary user persona (visitor, investor researcher, maintainer)?
- Who approves the plan vs who implements?
- Who resolves product tradeoffs if the user is unavailable?

## 5. Architecture and integration — B · E

- Where does this live in the stack (Eleventy template, data file, test, research CSV)?
- Upstream/downstream dependencies (build pipeline, Playwright, npm scripts)?
- New abstractions vs extending existing modules?
- Config vs code vs content — which layer owns the change?
- Subagent waves needed? Disjoint ownership table required?

## 6. Data and content — B · E

- New data files, schema changes, or migrations?
- Source of truth — repo, external API, manual CSV?
- Idempotency and regeneration (build output in `dist/` never hand-edited)?
- Research vs site content boundary respected?

## 7. UX and behavior — E

- Happy path walkthrough in one sentence?
- Error, empty, and loading states?
- Accessibility (keyboard, contrast, semantics)?
- Mobile vs desktop priority?
- Content tone and locale (Kenya market, investor audience)?

## 8. API and external services — E

- New MCP, HTTP, or third-party integration?
- Auth, rate limits, fallback when service is down?
- Secrets handling (`.env`, never commit)?

## 9. Testing and quality — B · E

- Which test layer fits ([docs/testing-reference.md](../../../docs/testing-reference.md)) — unit, integration, smoke, full E2E?
- Minimum gate before merge (`npm run test:smoke`, `npm test`, lint)?
- Senior review or Playwright design QA required?
- Manual validation steps if no automated coverage?

## 10. Rollout and risk — B

- Feature flag, phased rollout, or big-bang?
- Rollback plan?
- Worst realistic failure mode?
- `[needs validation]` items that block ship?

## 11. Alternatives — S unless high stakes

- Why this approach vs the obvious alternative?
- Reversible decision or one-way door?
- What would we prototype first if time were halved?

## 12. Handoff — B

- Plan approval criteria — what must the user sign off on?
- Todos/waves for Agent mode execution?
- Open questions deferred to implementation?

---

## Ordering heuristic

```
Goal → Scope → Constraints → Architecture → Data → Testing → Rollout → Alternatives (if needed) → Handoff
```

Within a branch, ask parent decisions before child decisions (e.g. "MVP scope" before "button color").

## Codebase shortcuts (explore, don't ask)

When planning site work, prefer readonly checks for:

- Stack and test commands → `AGENTS.md`
- Template patterns → `eleventy/src/`
- Existing tests → `tests/`
- Agent workflow → `docs/agent-and-subagent-workflow.md`
- Research boundaries → `research/AGENTS.md`

State findings as confirmations: "AGENTS.md specifies smoke tests after CSS changes — I'll gate on `npm run test:smoke`. OK?"
