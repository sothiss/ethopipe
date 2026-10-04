# Cross-Model Agent Handoff & Catch-Up Workflow

## Overview & Purpose

When developing **EthoPipe**, you may leverage different paid AI models depending on their specialized strengths:
- **Anthropic Claude (3.5 Sonnet / Opus)**: Exceptional at nuanced Python refactoring, strict linguistic de-biasing, and multi-file code editing.
- **OpenAI (o1 / o3-mini / GPT-4o)**: Powerful reasoning for complex mathematical modeling, hypothesis boundary generation, and schema verification.
- **Google Gemini (Gemini 3.5 / 3.8 Flash & Pro)**: Rapid turnaround, massive token context, and rich workspace integration within Antigravity IDE.
- **Cursor / Aider**: In-editor and CLI interactive pair programming.

This workflow eliminates friction and context drift when switching between models mid-task or across work sessions. It provides an automated, one-command mechanism to capture exact repository state, compile fresh code context, and generate a standardized catch-up prompt ready for instant pasting.

---

## What the Workflow Generates

When triggered, the workflow produces three key artifacts:

1. **`docs/AGENT_HANDOFF.md` (and `docs/handoffs/HANDOFF_<timestamp>.md`)**:
   A comprehensive Markdown status report detailing active branch, recent commits, uncommitted diffs, test pass/fail state, and clear next steps.
2. **`docs/LLM_SNAPSHOT.md`**:
   An updated, concatenated single-file compilation of all first-party Python source files and project configuration files (via `scripts/compile_snapshot.py`).
3. **Clipboard-Ready Catch-Up Prompt (`<CONTEXT_HANDOFF>`)**:
   A compact, structured prompt automatically copied to your Windows clipboard and printed to the terminal, specifically formatted to prime any incoming LLM agent with persona, project invariants, active telemetry, and next actions.

---

## Quick Start: How to Switch Models

### Step 1: Generate the Handoff in Your Current Session

Run either of the following commands from your project root:

#### Using PowerShell (Recommended):
```powershell
.\scripts\handoff.ps1 -Objective "Fixing parser timestamp validation" -NextSteps "1. Add test case for ISO 8601`n2. Update parser.py`n3. Run pytest" -RunTests -UpdateSnapshot
```

#### Using Python Directly:
```bash
python scripts/generate_agent_handoff.py --objective "Fixing parser timestamp validation" --next-steps "1. Add test case for ISO 8601\n2. Update parser.py\n3. Run pytest" --run-tests --update-snapshot --copy
```

#### From Within Antigravity IDE Chat:
Simply tell the active agent:
> *"I need to switch to Claude (or OpenAI). Please generate an agent handoff report for objective: [Your Objective]."*

The agent will execute the `agent-handoff` workflow and confirm clipboard copy.

---

### Step 2: Paste into the Incoming Model

Open your target agent UI or CLI:

#### A. Claude Code / Anthropic Web UI (Claude 3.5 Sonnet / Opus)
1. Open a new chat or terminal session.
2. Press `Ctrl + V` to paste the clipboard content.
3. (Optional) If using Claude web or Claude Project, you can also attach or reference `docs/LLM_SNAPSHOT.md` or `docs/AGENT_HANDOFF.md`.
4. Claude will immediately acknowledge the state, confirm invariants, and begin executing the specified next actions.

#### B. OpenAI (ChatGPT Plus/Team / o1 / GPT-4o)
1. Start a new chat session.
2. Press `Ctrl + V` to paste the prompt.
3. The prompt explicitly informs the model of Pydantic v2 strict configuration, physiological heart rate bounds (30–250 BPM), Darwin Core compliance, and tests.

#### C. Cursor or Aider
1. In Cursor Composer / Chat (`Ctrl + I` or `Ctrl + L`), paste the `<CONTEXT_HANDOFF>` block.
2. Type `@docs/AGENT_HANDOFF.md` or `@docs/LLM_SNAPSHOT.md` if additional file context is needed.

#### D. Returning to Antigravity
1. In Antigravity IDE, when starting a new session or switching back to Gemini, simply provide the latest `docs/AGENT_HANDOFF.md` or run `.\scripts\handoff.ps1`.

---

## Core Invariants Enforced Across All Models

Every generated handoff primes the incoming agent with EthoPipe's mandatory non-negotiable rules:
1. **Pydantic v2 Strict Mode**: `model_config = ConfigDict(strict=True)` enforced on all models.
2. **Physiological Boundaries**: Canine heart rates strictly clamped to `30–250` BPM (Toy: `80–200` BPM; Giant: `40–110` BPM).
3. **Darwin Core (DwC) Standardization**: Observations mapped to `MeasurementOrFact` with `dwc:individualID`, `dwc:eventDate`, `dwc:measurementType`, `dwc:measurementValue`, `dwc:basisOfRecord`.
4. **Linguistic Neutrality**: Subjective anthropomorphic terms ('stubborn', 'spiteful', 'angry') scrubbed from extraction pipelines.
5. **Quality Verification**: Full test suite pass verification (`pytest tests/`).

---

## Script Parameters Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `-Objective` / `--objective` | string | Standardizing workflows | Immediate micro-objective for the next agent |
| `-Completed` / `--completed` | string | Auto-summary | Work accomplished in the current session |
| `-InProgress` / `--in-progress` | string | Auto-summary | In-flight or uncommitted work |
| `-NextSteps` / `--next-steps` | string | Step-by-step list | Exact actions for the incoming model to execute |
| `-Blockers` / `--blockers` | string | None | Known warnings, edge cases, or pitfalls |
| `-Notes` / `--notes` | string | Target model notes | Directives or architectural caveats |
| `-TargetAgent` / `--target-agent`| string | Any | Target model family (Claude, OpenAI, Cursor, etc.) |
| `-RunTests` / `--run-tests` | switch | False | Executes pytest and records live test pass/fail output |
| `-UpdateSnapshot` / `--update-snapshot`| switch | False | Recompiles `docs/LLM_SNAPSHOT.md` |
| `-NoCopy` (PowerShell) | switch | False | Skips automatic Windows clipboard copying |
| `--copy` (Python) | flag | False | Explicitly copies prompt to Windows clipboard |
