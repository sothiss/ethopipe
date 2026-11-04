# Autonomous Code Companion Workflow

## Overview & Purpose

Asynchronous coding agents and subagents—such as **Antigravity subagents**, **GitHub Copilot coding agent**, **Claude Code**, and **Cursor background agents**—operate without mid-turn interactive dialogue:
- They execute scoped tasks on feature branches (`feature/...`, `perf/...`, `security/...`).
- They open Pull Requests or return verified diffs upon completion.
- In EthoPipe, companion briefs support specialized operational tracks:
  - ⚡ **Bolt** (`bolt`): Algorithmic performance, caching, and serialization speedups.
  - 🛡️ **Sentinel** (`sentinel`): Input hardening, boundary defense, and PII protection.
  - 🧪 **Test** (`test`): Hypothesis property-based and adversarial boundary testing.
  - 📦 **Feature** (`feature`): Darwin Core extensions and pipeline processing.
  - 🔧 **Refactor** (`refactor`): Simplification and `< 600` line modularization.

Because background agents operate autonomously during their turn, delegating tasks requires **mechanistic, strictly bounded task briefs** with explicit file permissions and non-negotiable invariant checklists.

---

## How to Delegate a Task to an Autonomous Agent

### 1. Generate the Task Brief

Run the handoff runner with the `-Companion` flag from PowerShell:

#### A. Performance Optimization Task (⚡ Bolt)
```powershell
.\scripts\handoff.ps1 -Companion -CompanionType bolt `
    -Objective "Optimize CanineObservation deserialization with pre-computed regex lookup" `
    -TargetFiles "src/pipeline/models.py,tests/test_models.py" `
    -RunTests
```

#### B. Security / Boundary Hardening Task (🛡️ Sentinel)
```powershell
.\scripts\handoff.ps1 -Companion -CompanionType sentinel `
    -Objective "Clamp maximum string length for handler_notes to prevent memory exhaustion" `
    -TargetFiles "src/pipeline/models.py,tests/test_models.py" `
    -RunTests
```

#### Or via Python:
```bash
python scripts/generate_agent_handoff.py --companion --companion-type bolt \
    --objective "Optimize CanineObservation deserialization" \
    --target-files "src/pipeline/models.py,tests/test_models.py" \
    --run-tests --copy
```

### 2. Dispatch the Task Brief

The task brief is automatically copied to your clipboard and saved in `docs/COMPANION_TASK.md`.

1. **GitHub Issue / Subagent Delegation**: Paste (`Ctrl + V`) into a GitHub Issue or subagent prompt.
2. **Included Guardrails**:
   - Recommended Conventional Commit PR title (`perf(pipeline): ...`, `fix(pipeline): ...`)
   - Strict list of permitted files (forbidding unauthorized config modifications)
   - Step-by-step implementation tasks
   - EthoPipe invariants (Pydantic v2 strict, canine HR 30-250 BPM, Darwin Core, linguistic neutrality)
   - Mandatory verification commands (`pytest tests/`, `ruff check`, `ruff format --check`, `mypy src`)

---

## Reviewing an Autonomous Pull Request

Before merging a companion PR:
1. **Scope Check**: Confirm changed files match the authorized `TargetFiles` list.
2. **Invariants**: Confirm Pydantic models maintain `ConfigDict(strict=True)` and canine heart rates remain bounded `[30, 250]` BPM.
3. **Chronicle Logging**: Record significant architectural or security milestones in `JOURNEY.md` or `CHANGELOG.md`.
4. **Local QA Verification**: Run `.\scripts\run_qa.ps1` before merging.
