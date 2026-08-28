# Context budget log — {project-slug}

Coordinator context tracking for multi-agent research runs. Parent agents should stay under ~**85%** context ([`docs/agent-and-subagent-workflow.md`](../../../../docs/agent-and-subagent-workflow.md)).

| Timestamp | Agent | Action | Est. context note |
|-----------|-------|--------|-------------------|
| YYYY-MM-DD | Coordinator | Init tree, methodology, INDEX | ~15% — stubs only |
| YYYY-MM-DD | SA-1 | *(handoff summary only — no file dumps)* | ~25% — handoff only |

**Rules:**

- Record **handoffs**, not raw deliverable contents.
- Workers return structured summaries; parent ingests ≤15 lines prose per wave.
- If parent context exceeds ~85%, stop spawning — merge and close the wave.
