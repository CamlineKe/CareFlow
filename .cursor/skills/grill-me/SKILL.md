---
name: grill-me
description: >-
  Default Plan mode workflow — stress-test plans and designs via structured
  questions until shared understanding. Use in Plan mode, when the user wants
  to get grilled, stress-test a design, or mentions "grill me". User may skip
  with "Work with assumptions".
---

# Grill me

Adapted from [mattpocock/skills — grill-me](https://github.com/mattpocock/skills/blob/733d312884b3878a9a9cff693c5886943753a741/skills/productivity/grill-me/SKILL.md).

## Plan mode default

**Every Plan mode session** starts here before drafting or editing a plan.

### Opening choice (required once per session)

Present this block at the start of planning work:

```
Before we plan, choose one:

1. **Grill me** (default) — resolve open decisions question-by-question until we share understanding.
2. **Work with assumptions** — skip grilling; document assumptions and proceed with the plan.
```

| Path | When | Agent behavior |
|------|------|----------------|
| **Grill me** | User picks this, stays silent on choice, or keeps adding requirements | Run the full grill workflow below |
| **Work with assumptions** | User says **Work with assumptions** (exact phrase) or clearly asks to skip questions | Skip grilling; emit Assumptions block; proceed |

Do not re-offer the choice after the user has picked a path unless they explicitly restart planning.

## Work with assumptions

When the user chooses **Work with assumptions**:

1. **Do not** run sequential grilling.
2. Emit an **Assumptions** section before the plan:

```markdown
## Assumptions

- [assumption] — [brief rationale]
- [assumption] — [brief rationale] `[needs validation]`  ← high-risk or product-facing
```

3. Mark assumptions as `[needs validation]` when wrong guess would change scope, architecture, UX, compliance, or rollout.
4. Proceed to plan synthesis; treat assumptions as provisional until the user corrects them.

If the user later contradicts an assumption, update the Assumptions section and re-check dependent plan sections — do not restart the full grill unless they ask.

## Grill workflow

Interview relentlessly about every aspect of the plan until shared understanding. Walk each branch of the design tree; resolve dependencies between decisions one-by-one.

### 1. Inventory (silent)

Before the first question:

1. Parse the user goal, constraints, and any existing plan/docs.
2. Read [reference/question-tree.md](./reference/question-tree.md) and select **only** applicable branches.
3. **Explore the codebase** (readonly) for answers — remove those from the queue.
4. Order remaining questions: **blocking dependencies first**, then scope, then polish.
5. Keep a mental **Decisions log** (surface it when useful).

Do not dump the full question list on the user. Use the inventory to stay exhaustive without feeling exhaustive.

### 2. Ask one at a time

For each question:

- Ask **one** question only.
- Include your **recommended answer** (one paragraph max).
- If the user accepts the recommendation, record the decision and move on.
- If they disagree, record their choice and adjust downstream questions.

**Never** ask a question whose answer is discoverable in the repo — explore instead, then state what you found and confirm.

### 3. Close the grill

When all branches are resolved:

1. Summarize **Decisions** (bullet list).
2. List **Deferred** items explicitly (out of scope or Phase 2).
3. Hand off to plan synthesis per [docs/agent-sops/plan.md](../../../docs/agent-sops/plan.md).

## Question quality bar

Smart exhaustion means **complete coverage, minimal noise**:

| Do | Don't |
|----|-------|
| Ask decisions that change the plan | Ask trivia already in AGENTS.md or obvious from stack |
| Collapse redundant questions | Ask five questions about the same tradeoff |
| Front-load irreversible choices | Start with naming or cosmetic details |
| Stop when remaining gaps are low-risk | Grill past diminishing returns |

## Mode

**Plan mode only** for the default workflow — readonly discovery; no file writes.

Implementation belongs in **Agent** mode after the plan and Decisions/Assumptions are accepted.

## Triggers outside Plan mode

Also apply when the user explicitly asks to stress-test a plan, "grill me", or resolve design ambiguity before building — but still offer **Work with assumptions** once at the start.

## Anti-patterns

- Skipping the opening choice in Plan mode
- Batch-asking multiple questions in one message
- Writing scaffold files during the grill
- Treating **Work with assumptions** as "ask no questions ever" — clarifying contradictions is still allowed
