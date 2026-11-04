# EthoPipe AI Task & Walkthrough Evolution Archive

This directory stores immutable, version-controlled snapshots of AI pair-programming **Task Checklists** and **Post-Execution Walkthroughs** (`WALKTHROUGH_YYYYMMDD_HHMMSS_<topic>.md`).

## 🎯 Why This Archive Exists

While Google Antigravity IDE renders `task.md` and `walkthrough.md` inside its local AppData directory (`~/.gemini/antigravity/brain/<conversation-id>/`), machine-local artifacts are not tracked by Git. Archiving unified Task + Walkthrough snapshots here guarantees a permanent, reproducible research record of:
1. **Model & Harness Evolution**: How successive generations of **Gemini** inside **Google Antigravity IDE** (from Gemini 1.5/2.5/3.1/3.5/3.8 through Gemini 4+) decompose engineering problems over time.
2. **Task Deconstruction Fidelity**: Exact `[x]` micro-task plans before and after implementation.
3. **Cognitive & Architectural Reasoning**: Trade-offs, bug discoveries, Solo Maintainer Charter enforcement, and verification proofs.

---

## 🛠️ Management Commands

```powershell
# 1. Archive a session's Task + Walkthrough files into docs/walkthroughs/:
.\scripts\journey.ps1 -Archive -Title "Solo Workflow Pruning" `
    -Model "Gemini 4 (Medium)" `
    -TaskFile "<path-to-task.md>" `
    -WalkthroughFile "<path-to-walkthrough.md>"

# 2. List all archived walkthroughs & JOURNEY.md entries:
.\scripts\journey.ps1 -List

# 3. Record a milestone in JOURNEY.md cross-linked to an archived walkthrough:
.\scripts\journey.ps1 -New "Milestone Title" -Model "Gemini 4 (Medium)" `
    -WalkthroughRef "docs/walkthroughs/WALKTHROUGH_YYYYMMDD_HHMMSS_slug.md" ...
```

*For the chronological executive narrative across all project phases since 2025, see [**`JOURNEY.md`**](../../JOURNEY.md).*
