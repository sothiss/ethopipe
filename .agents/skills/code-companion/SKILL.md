---
name: code-companion
description: Generates strictly scoped, deterministic task briefs and prompts tailored for asynchronous code companions such as Google Labs Jules, GitHub Copilot Workspace, or Devin, enforcing repository invariants and .jules/ learning journal updates.
---

# Code Companion (Jules) Skill

Use this skill when delegating tasks, bugfixes, or refactoring jobs to asynchronous code companions like **Google Labs Jules** (`@google-labs-jules[bot]`).

## Trigger Command

To generate a task prompt for Jules or a code companion:

### PowerShell
```powershell
.\scripts\handoff.ps1 -Companion -CompanionType bolt -Objective "<Optimization objective>" -TargetFiles "src/pipeline/models.py,tests/test_models.py" -RunTests
```

### Python
```bash
python scripts/generate_agent_handoff.py --companion --companion-type sentinel --objective "<Security/Sanitization objective>" --target-files "src/pipeline/models.py" --run-tests --copy
```

## Supported Companion Tracks
- `bolt`: Performance optimizations -> enforces updating `.jules/bolt.md` and PR prefix `⚡ Bolt:`.
- `sentinel`: Security & boundary validations -> enforces updating `.jules/sentinel.md` and PR prefix `🛡️ Sentinel:`.
- `test`: Test suite expansion / Hypothesis property testing -> PR prefix `test:`.
- `feature`: Darwin Core / API feature additions -> PR prefix `feat:`.

## Outputs
- `docs/JULES_TASK.md`: The complete markdown issue / task brief.
- Clipboard: The exact prompt block ready to paste into GitHub Issue / Jules UI.
