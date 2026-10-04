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

## Code Companions (Jules & Autonomous Agents)

When delegating tasks to autonomous code companions (e.g., Google Labs Jules `@google-labs-jules[bot]`):

1. **Generate Task Brief**: Run `.\scripts\handoff.ps1 -Jules -CompanionType bolt -Objective "<Objective>" -TargetFiles "<Files>"` (or `-CompanionType sentinel`).
2. **Review Brief**: Inspect `docs/JULES_TASK.md` and paste the clipboard prompt into the GitHub Issue or companion prompt.
3. **Journal Maintenance**: Ensure the companion updates `.jules/bolt.md` (for performance) or `.jules/sentinel.md` (for security).
4. **Documentation**: See `docs/CODE_COMPANION_WORKFLOW.md` for full instructions.

## Solo Maintainer Guardrails & Anti-Bloat Policy

EthoPipe is strictly governed by the Solo Maintainer Charter to prevent cognitive overhead and dependency rot:

1. **Language Monoculture**: 100% pure Python (>= 3.11). Never introduce Node/npm, TypeScript, Rust, Go, or compiled C bindings.
2. **Dependency Cap**: Maximum of 8 direct runtime dependencies in `pyproject.toml`. Always prioritize the Python standard library.
3. **Prohibited Daemons**: Reject external message brokers (Redis, Celery, RabbitMQ), distributed frameworks (Kafka, Spark), and enterprise orchestrators (Airflow).
4. **Skill Hygiene**: Do not install enterprise cloud skills (BigQuery, Spark, Composer, Dataflow) in `.agents/skills`.
5. **Audit Enforcement**: Run `python scripts/audit_maintainer_guardrails.py` (or `.\scripts\run_qa.ps1`) before submitting or approving changes.

## Walkthrough & Task Protocol (Mandatory)

Every AI coding assistant (Gemini, Claude, GPT, Cursor) working in EthoPipe MUST strictly uphold the Task & Walkthrough invariant:

1. **Up-Front Tasks**: Deconstruct non-trivial requests into a trackable checklist (`[ ]`, `[/]`, `[x]`) before writing code.
2. **Post-Execution Walkthrough**: Always produce a structured Walkthrough detailing:
   - Executive summary and motivation.
   - Exact files changed with clickable links (`file:///...`).
   - Architectural thinking and AI cognitive journey (key decisions, trade-offs, constraints).
   - Verification proof (executed test commands and passing assertions).
3. **Rule Definition**: See `.agents/rules/walkthrough-and-tasks.md`.

## Session Journey Logging (AI Evolution & Architectural Decisions)

To record the technical journey and trace the evolution of AI model reasoning (coding predominantly with Gemini since 2025):

1. **Inspect / Append Journey**: Use `.\scripts\journey.ps1 -Template` or `python scripts/manage_journey.py new ...`.
2. **Chronicle Invariants**: Each session entry in `JOURNEY.md` logs the active model, architectural pivots, interesting cognitive steps taken by the AI, and verified milestones.
3. **Log Location**: See `JOURNEY.md` for complete historical logs.
