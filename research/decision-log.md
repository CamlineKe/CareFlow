# Research decision log

Cross-project **locked decisions**, **superseded paths**, and **risks** from prior research. Agents treat entries here as constraints during planning unless the user explicitly reopens a decision.

**Maintenance:** when an ops or big-picture project locks a conclusion, add a row here and mirror detail in that project's `meta/decision-log.md`. Implementation ADRs go to [`docs/research/`](../docs/research/) when code is affected.

| ID | Tier | Decision | Source | Status | Notes |
|----|------|----------|--------|--------|-------|
| *(add rows as projects lock decisions)* | | | | | |

## Known inconsistencies / open tensions

| Issue | Where | Agent action |
|-------|-------|--------------|
| *(none yet)* | | |

## How agents use this log

| Task type | Read this log? | Load big-picture deliverables? |
|-----------|----------------|--------------------------------|
| Pure ops implementation from existing spec | Yes — one table scan | No — use project's `meta/big-picture-brief.md` |
| New ops research | Yes | Summaries only via subagent brief |
| Plan mode / grill-me | Yes — surface as constraints | Subagent inconsistency check if scope touches market + stack |
| Big-picture-only research | Yes — avoid contradicting locked ops | N/A |

## Changelog

| Date | Change |
|------|--------|
| *(init)* | Empty starter log — populate as research projects complete |
