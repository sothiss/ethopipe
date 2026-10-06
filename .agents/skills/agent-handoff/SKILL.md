---
name: agent-handoff
description: Generates a comprehensive state report, telemetry summary, and ready-to-paste catch-up prompt to seamlessly switch development between AI models (Claude, OpenAI, Cursor, Antigravity) without context or invariant loss.
---

# Agent Handoff & Cross-Model Switching Skill

Use this skill whenever you or the user need to transition work to another model or agent, or when catching up after switching models.

## Quick Trigger Commands

To generate an automated handoff report, updated codebase snapshot, and clipboard-copied catch-up prompt:

### PowerShell
```powershell
.\scripts\handoff.ps1 -Objective "<Immediate Objective>" -Completed "<Summary>" -NextSteps "<Next Steps>" -RunTests -UpdateSnapshot
```

### Python Direct
```bash
python scripts/generate_agent_handoff.py --objective "<Objective>" --completed "<Summary>" --next-steps "<Next Steps>" --run-tests --update-snapshot --copy
```

## Generated Outputs
- `docs/AGENT_HANDOFF.md`: Latest state report and full telemetry.
- `docs/handoffs/HANDOFF_<timestamp>.md`: Immutable historical record of the handoff.
- `docs/LLM_SNAPSHOT.md`: Updated single-file aggregation of all repository code.
- Windows Clipboard: Populated with a formatted, self-contained `<CONTEXT_HANDOFF>` prompt block ready to paste into Claude, ChatGPT, Cursor, or Aider.

## Receiving a Handoff as an Incoming Agent
When receiving a handoff:
1. Parse the `<CONTEXT_HANDOFF>` block.
2. Read `docs/AGENT_HANDOFF.md` for extended telemetry and diff context.
3. Confirm active branch and git status.
4. Adhere strictly to EthoPipe domain invariants (Pydantic v2 strict, canine HR [30, 250], Darwin Core DwC, linguistic de-biasing).
5. Execute the listed immediate NEXT ACTIONS.
