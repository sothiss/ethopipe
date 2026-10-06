---
name: jules
description: Specialized implementation of the EthoPipe Code Companion protocol for Google Labs Jules (@google-labs-jules[bot]).
---

# Jules (Google Labs Code Companion) Skill

This skill is the specialized implementation of the EthoPipe Code Companion protocol for **Google Labs Jules** (`@google-labs-jules[bot]`).

See full instructions in [`.agents/skills/code-companion`](file:///H:/Projects/ethopipe/.agents/skills/code-companion/SKILL.md).

## Quick Command for Jules Tasks
```powershell
.\scripts\handoff.ps1 -Companion -CompanionType bolt -Objective "<Task Objective>" -TargetFiles "<File list>" -RunTests
```
This automatically prepares a structured issue brief, enforces the `.jules/bolt.md` or `.jules/sentinel.md` journal protocol, and copies the prompt to your clipboard.
