---
name: code-companion
description: Generates strictly scoped, deterministic task briefs and prompts tailored for asynchronous coding agents and subagents (Antigravity subagents, GitHub Copilot coding agent, Claude Code), enforcing repository invariants.
---

# Autonomous Code Companion Skill

Use this skill when delegating scoped tasks, bugfixes, or refactoring jobs to asynchronous background coding agents or subagents.

## Trigger Command

To generate a deterministic task brief:

### PowerShell
```powershell
.\scripts\handoff.ps1 -Companion -CompanionType bolt -Objective "<Optimization objective>" -TargetFiles "src/pipeline/models.py,tests/test_models.py" -RunTests
```

### Python
```bash
python scripts/generate_agent_handoff.py --companion --companion-type sentinel --objective "<Security/Sanitization objective>" --target-files "src/pipeline/models.py" --run-tests --copy
```

## Supported Companion Tracks
- `bolt`: Performance optimizations -> PR prefix `perf(pipeline):` / `⚡ Bolt:` and milestone note in `JOURNEY.md`.
- `sentinel`: Security & boundary validations -> PR prefix `fix(pipeline):` / `🛡️ Sentinel:` and milestone note in `JOURNEY.md`.
- `test`: Test suite expansion / Hypothesis property testing -> PR prefix `test:`.
- `feature`: Darwin Core / API feature additions -> PR prefix `feat:` and entry in `CHANGELOG.md`.
- `refactor`: Simplification and `< 600` line modularization -> PR prefix `refactor:`.

## Outputs
- `docs/COMPANION_TASK.md`: The complete markdown issue / task brief.
- Clipboard: The exact prompt block ready to paste into a GitHub Issue or subagent prompt.
