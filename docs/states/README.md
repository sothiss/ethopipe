# EthoPipe Historical Project State & Checkpoint Archive

This directory stores immutable, timestamped snapshots of EthoPipe's project goals and working states (`STATE_YYYYMMDD_HHMMSS.md`).

## 🎯 Purpose & Invariants

Whenever a development session finishes, pauses, or pivots, a checkpoint snapshot is created here. This solves the core solo developer and AI handoff challenge: **knowing exactly where work was stopped and how to resume instantly without context loss.**

Each checkpoint preserves:
1. **Timestamp & Commit**: Exact date/time and Git commit hash when work paused.
2. **Current Focus**: The active milestone or feature under construction.
3. **Stopping Point (`Where We Stopped`)**: Specific modules, lines of code, or tasks left in progress.
4. **Quick-Resume Action (`Next Action`)**: The immediate first command or code change to run upon resuming.
5. **Goals Roadmap**: Immediate sprint tasks, near-term goals, and long-term milestones.

---

## 🛠️ Management Commands

```powershell
# 1. View current project state & quick-resume command:
.\scripts\state.ps1

# 2. Record a new checkpoint:
.\scripts\state.ps1 -Checkpoint -Focus "<Focus>" -StoppedAt "<Where Work Stopped>" -NextStep "<What To Do Next>"

# 3. View historical checkpoints:
.\scripts\state.ps1 -History
```

*For live active state, consult [**`docs/PROJECT_STATE.md`**](../PROJECT_STATE.md).*
