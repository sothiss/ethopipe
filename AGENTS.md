<!-- gitbook-agent-instructions:start -->

## GitBook Documentation Editing

This repository contains documentation synced with GitBook via Git Sync.

Before editing GitBook-synced Markdown, YAML, or asset files, make sure the GitBook skill is available and up to date in your local agent environment. Prefer installing or updating it with:

```bash
npx skills add gitbookio/gitbook-skills
```

This command may add or update local agent skill files. Use them only as local agent instructions; do not commit those installed skill files or any tool-generated agent configuration unless the user explicitly asks for it.

If `npx` is unavailable, load the skill from:

https://gitbook.com/docs/skill.md

When making changes, preserve GitBook sync metadata such as frontmatter, `SUMMARY.md`, `gitbook-docs.yaml`, `.gitbook/`, and asset links unless the requested edit explicitly requires changing them.

<!-- gitbook-agent-instructions:end -->

## Cross-Model Agent Handoff & Catch-Up

When switching active development between AI models (Antigravity/Gemini, Anthropic Claude, OpenAI o1/GPT-4o, Cursor):

1. **Generate Handoff**: Run `.\scripts\handoff.ps1` or `python scripts/generate_agent_handoff.py --run-tests --update-snapshot --copy`.
2. **Review State**: Read `docs/AGENT_HANDOFF.md` for live telemetry, active branch status, and recent diffs.
3. **Clipboard Prompt**: The formatted `<CONTEXT_HANDOFF>` prompt block is automatically copied to your clipboard to paste into the incoming model session.
4. **Workflow Documentation**: See `docs/AGENT_HANDOFF_WORKFLOW.md` for complete cross-agent instructions.
