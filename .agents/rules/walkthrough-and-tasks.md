---
trigger: always_on
---

# Mandatory Task Deconstruction, Walkthrough & AI Evolution Archive Rule

## Purpose
To maintain architectural clarity, preserve context across sessions, and permanently chronicle the evolution of **Gemini & Google Antigravity** (and peer AI models) throughout EthoPipe's lifecycle, every AI coding assistant MUST follow the **Task, Walkthrough & Repository Archiving Protocol** during every non-trivial session.

---

## 1. Up-Front Task Deconstruction
Before modifying source files or running destructive commands, outline an explicit, trackable checklist of micro-tasks:
1. **Explicit Checkpoints**: Break requests into sequential, verifiable sub-tasks naming exact files or verification commands.
2. **State Tracking**: Track live progress using GitHub-flavored markdown (`[ ]` not started, `[/]` in progress, `[x]` completed/verified).
3. **Antigravity UI Artifact**: In Antigravity IDE, maintain the live checklist in `<appDataDir>/brain/<conversation-id>/task.md`.

---

## 2. Mandatory Post-Execution Walkthrough
Every completed unit of work or session closeout MUST produce a structured **Walkthrough** containing:
1. **Executive Objective**: 1–2 sentences summarizing what was solved and why.
2. **Key Changes & Artifacts**: Clickable `file:///` links delineating created, modified, and removed files.
3. **AI Architectural Thinking & Cognitive Path**: Record *how* the model reasoned—alternatives weighed, edge cases caught, self-corrections, and Solo Maintainer / ethological invariants upheld.
4. **Verification & Proof of Correctness**: Exact commands executed (`ruff`, `mypy`, `pytest`, `audit_maintainer_guardrails.py`) and pass counts.
5. **Next Actions / Handoff**: Immediate next step for the Principal Investigator (`@sothiss`).

---

## 3. Permanent In-Repository Archiving (`docs/walkthroughs/` & `JOURNEY.md`)
Because IDE scratchpads (`~/.gemini/antigravity/brain/`) live outside Git version control, **every non-trivial session MUST also persist its Task Checklist & Walkthrough inside the repository**:

1. **Archive Unified Session Snapshot (`docs/walkthroughs/`)**:
   - Save a dated snapshot to `docs/walkthroughs/WALKTHROUGH_YYYYMMDD_HHMMSS_<kebab-topic>.md` (either directly or via `.\scripts\journey.ps1 -Archive ...` / `python scripts/manage_journey.py archive ...`).
   - Include a metadata header recording **Date**, **IDE/Harness** (e.g., `Google Antigravity IDE`), and **Active Model** (human-readable model name), followed by both the completed **Task Checklist** and **Walkthrough**.
2. **Link in `JOURNEY.md`**:
   - When logging a milestone in `JOURNEY.md` (`.\scripts\journey.ps1 -New ... --walkthrough-ref docs/walkthroughs/...`), cross-link the archived walkthrough file so future researchers and maintainers can inspect the full task decomposition and AI cognitive trace alongside the high-level chronicle.
