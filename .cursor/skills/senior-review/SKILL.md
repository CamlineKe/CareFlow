---
name: senior-review
description: >-
  Runs structured senior or PR code review in Ask mode using the project
  review schema. Use when the user requests code review, PR review, or
  @senior-code-review.
disable-model-invocation: true
---

# Senior review

## When to use

- User asks for senior/staff/PR/code review on named paths, globs, directories, or snippets
- After a feature slice, before expensive E2E gates
- Triggered via `@.cursor/rules/senior-code-review.mdc` or `/senior-review` (Claude Code)

## Mode

**Ask mode only** — read code; produce the review; **no** tool-driven edits in this thread.

Implementation fixes belong in a separate **Agent** session.

## Steps

1. Resolve scope → substitute for **`$ARGUMENTS`** in `.claude/commands/senior-review.md`
2. Read actual code (and nearby patterns); do not invent findings
3. Output using the schema for **`alex`**:
   - `alex` → [reference/97-things-output.md](./reference/97-things-output.md)
   - `severity-tier` → [reference/severity-tier-output.md](./reference/severity-tier-output.md)
4. If scope is missing, ask **once** for paths, glob, directory, or snippet

## Persona

Default reviewer persona: **Alex** (see command file for tone and stack checks).

## Stack

Enforce **generic** conventions from **AGENTS.md** during review.

## Anti-patterns

- Do not mix deep review and patching in one Agent thread
- Do not pad with generic praise
- Scale review length to diff size
