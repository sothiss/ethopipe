# Code Companion Workflow (Jules & Autonomous Coding Agents)

## Overview & Purpose

Autonomous code companions—most notably **Google Labs Jules** (`@google-labs-jules[bot]`), GitHub Copilot Workspace, and Devin—operate asynchronously:
- They work in single execution turns on background branches (e.g. `jules-...`).
- They create Pull Requests without interactive dialogue during implementation.
- In this repository, Jules maintains specialized operational tracks:
  - ⚡ **Bolt**: Algorithmic performance, caching, and serialization speedups.
  - 🛡️ **Sentinel**: Input hardening, boundary defense, and PII protection.
  - 🧪 **Test**: Hypothesis and adversarial boundary testing.
  - 📦 **Feature**: Darwin Core extensions and pipeline processing.

Because companions lack interactive mid-task feedback, delegating tasks requires **mechanistic, strictly bounded task briefs** with explicit file permissions and non-negotiable invariant checklists.

---

## The Jules Learning Journal (`.jules/`)

Jules maintains persistent repository knowledge in the `.jules/` directory:
- **[`bolt.md`](file:///H:/Projects/ethopipe/.jules/bolt.md)**: Records performance learnings and optimizations.
- **[`sentinel.md`](file:///H:/Projects/ethopipe/.jules/sentinel.md)**: Records security vulnerabilities, edge-case attacks, and sanitization boundaries.

Every task delegated under the Bolt or Sentinel tracks instructs the companion to append a structured entry upon completion:

```markdown
## YYYY-MM-DD - <Topic>
**Learning:** <Quantitative or architectural discovery>
**Action:** <Code change implemented>
```

---

## How to Delegate a Task to Jules / Code Companions

### 1. Generate the Task Brief

Run the handoff runner with the `-Jules` / `-Companion` flag from PowerShell:

#### A. Performance Optimization Task (⚡ Bolt)
```powershell
.\scripts\handoff.ps1 -Jules -CompanionType bolt `
    -Objective "Optimize CanineObservation deserialization with pre-computed regex lookup" `
    -TargetFiles "src/pipeline/models.py,tests/test_models.py" `
    -RunTests
```

#### B. Security / Boundary Hardening Task (🛡️ Sentinel)
```powershell
.\scripts\handoff.ps1 -Jules -CompanionType sentinel `
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

### 2. Paste the Task Brief

The task brief is automatically copied to your clipboard and saved in [`docs/JULES_TASK.md`](file:///H:/Projects/ethopipe/docs/JULES_TASK.md).

1. **GitHub Issue / Task Delegation**: Create a new GitHub issue or dispatch a prompt to Jules.
2. **Paste (`Ctrl + V`)**: The brief contains:
   - Recommended PR title (e.g. `⚡ Bolt: ...` or `🛡️ Sentinel: ...`)
   - Strict list of permitted files (forbidding config file modifications)
   - Step-by-step implementation tasks
   - EthoPipe invariants (Pydantic v2 strict, canine HR 30-250 BPM, Darwin Core, linguistic neutrality)
   - Mandatory verification commands (`pytest tests/`, `ruff check`, `ruff format --check`)
   - Mandatory journal update instructions for `.jules/`

---

## Reviewing a Companion Pull Request

When Jules opens a PR:
1. **Scope Check**: Confirm that files changed match the authorized `TargetFiles` list.
2. **Invariants**: Confirm Pydantic models maintain `ConfigDict(strict=True)` and canine heart rates are bounded.
3. **Journal Verification**: Confirm that `.jules/bolt.md` or `.jules/sentinel.md` has been updated with a new entry.
4. **Local QA Verification**: Run `.\scripts\run_qa.ps1` before merging.
