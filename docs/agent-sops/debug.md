# Debug mode SOP

| Field | Guidance |
|-------|----------|
| **Purpose** | Find root cause and minimal fix for a specific failure |
| **Allowed** | Narrow repro commands; readonly log/trace subagent; then scoped edits |
| **Default workflows** | Narrow repro → classify layer → minimal fix → re-run narrow → broaden |
| **Context budget** | ~90% for implementer; delegate log parsing to `debugger` / readonly subagent |
| **Handoffs** | Stable fix + test → **Ask** optional review; structural issue → **Plan** |
| **Invoke** | Debug mode; “flaky test”, “regression in X”, CI failure with logs |
| **Anti-patterns** | Full test suite + multi-module refactor; fixing symptoms without repro; skipping runner classification |
