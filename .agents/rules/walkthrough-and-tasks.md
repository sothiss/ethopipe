# Mandatory Task Deconstruction & Walkthrough Rule

## Purpose
To maintain architectural clarity, preserve context across sessions and AI models, and support solo maintainer sustainability, all AI assistants (Antigravity/Gemini, Claude, GPT, Cursor) and automated code companions MUST strictly follow the **Task & Walkthrough Protocol** during every non-trivial interaction.

---

## 1. Up-Front Task Deconstruction

Before modifying source files or running destructive commands, the AI agent MUST outline a clear, actionable checklist of micro-tasks.

### Requirements:
1. **Explicit Checkpoints**: Break user requests down into sequential, verifiable sub-tasks.
2. **State Tracking**: Keep track of task statuses using GitHub-flavored markdown:
   - `[ ]` Not started
   - `[/]` In progress
   - `[x]` Completed / verified
3. **No Phantom Tasks**: Avoid vague bullets. Every task must state the specific artifact, file, or verification step involved.

---

## 2. Mandatory Post-Execution Walkthrough

Every completed unit of work or session closeout MUST include a structured **Walkthrough** artifact or response section.

### Walkthrough Schema:
1. **Executive Objective**: 1-2 sentences summarizing what was solved and why.
2. **Key Changes & Artifacts**:
   - Provide clickable file links using `file:///` format (e.g., [`path/to/file.py`](file:///path/to/file.py#L1-L20)).
   - Clearly delineate created vs. modified files.
3. **AI Architectural Thinking & Cognitive Path**:
   - Record the *reasoning* that guided the solution: alternative options considered, edge cases detected, and deliberate trade-offs made.
   - Note any domain-specific insights (biological limits, solo maintainer budget, zero-bloat principles).
4. **Verification & Proof of Correctness**:
   - Explicitly cite the commands executed (e.g. `pytest`, `python scripts/audit_maintainer_guardrails.py`).
   - Quote test counts, pass rates, or benchmark timings.
5. **Next Actions / Handoff**:
   - Suggest the next immediate step or command for the human PI to run.

---

## 3. End-of-Session Journey Protocol

When closing out a work session, the agent should assist the PI in logging the session into [`JOURNEY.md`](file:///H:/Projects/ethopipe/JOURNEY.md) using `.\scripts\journey.ps1` or `python scripts/manage_journey.py` to ensure long-term historical tracking of AI evolution and engineering decisions.
