---
name: project-state
description: Tracks project goals, active working state, stopping points, and next resume steps, archiving dated historical checkpoints in docs/states/ to ensure frictionless resumption across sessions.
---

# EthoPipe Project Goals & State Management Skill

Use this skill whenever you or the user need to:
1. **Resume Development**: Understand where work stopped, what is finished, and what immediate next step to take.
2. **Record a Checkpoint**: Capture current progress, active stopping points, and next actions before taking a break or closing a session.
3. **Review Dated History**: Inspect historical checkpoints in `docs/states/` to trace project evolution and stopping points over time.
4. **Align on Goals**: Review or update the project goals roadmap (Immediate, Near-Term, Long-Term).

---

## ⚡ Quick Trigger Commands

### Inspect Current State & Quick-Resume Action
```powershell
.\scripts\state.ps1
```
*(or `python scripts/manage_project_state.py status`)*

### Record a Stopping Point Checkpoint
Whenever pausing or stopping work:
```powershell
.\scripts\state.ps1 -Checkpoint -Focus "<Milestone or Task Name>" -StoppedAt "<What was done & exact files/lines paused at>" -NextStep "<Immediate next action to resume>"
```
*(or `python scripts/manage_project_state.py checkpoint --focus "<Focus>" --stopped-at "<Where Stopped>" --next-step "<Next Step>" --goal "[ ] Goal 1" --goal "[x] Goal 2"`)*

### View Historical Checkpoint Timeline
```powershell
.\scripts\state.ps1 -History
```
*(or `python scripts/manage_project_state.py history`)*

---

## 📂 Managed Artifacts

- **Live State Document**: [`docs/PROJECT_STATE.md`](../../docs/PROJECT_STATE.md)
  Authoritative single source of truth for active focus, stopping point, quick-resume command, and goals roadmap.
- **Historical Checkpoint Snapshots**: [`docs/states/STATE_YYYYMMDD_HHMMSS.md`](../../docs/states/)
  Immutable dated records capturing exact branch, git commit, dirty file count, stopping point, and goals at that moment.

---

## 🔄 Resumption Protocol (Incoming Agent or Maintainer)

When starting or resuming a session:
1. **Check Live State**: Run `.\scripts\state.ps1` or read `docs/PROJECT_STATE.md`.
2. **Review Stopping Point**: Note what was completed and what files were left in progress.
3. **Execute Quick-Resume Action**: Immediately run the suggested command or begin the outlined task.
4. **Before Leaving**: Always record a fresh checkpoint via `.\scripts\state.ps1 -Checkpoint ...`.
