#!/usr/bin/env python3
"""
EthoPipe Agent Handoff & Code Companion Task Generator

Generates state reports, telemetry summaries, and tailored prompts for:
1. Interactive Cross-Model Handoffs (Claude, OpenAI o1/4o, Cursor, Antigravity)
2. Autonomous Code Companions (Google Labs Jules, GitHub Copilot Workspace, Devin)
"""

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Execute a system command and return (exit_code, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as exc:
        return 1, "", str(exc)


def get_git_telemetry(project_root: Path) -> dict[str, str]:
    """Gather git version control state and diffs."""
    telemetry: dict[str, str] = {}

    # Active branch
    code, out, _ = run_cmd(["git", "branch", "--show-current"], cwd=project_root)
    telemetry["branch"] = out if code == 0 and out else "unknown"

    # Latest commit
    code, out, _ = run_cmd(
        ["git", "log", "-1", "--pretty=format:%h - %s (%an, %ar)"],
        cwd=project_root,
    )
    telemetry["latest_commit"] = out if code == 0 else "None"

    # Recent history
    code, out, _ = run_cmd(
        ["git", "log", "-n", "5", "--oneline"],
        cwd=project_root,
    )
    telemetry["recent_commits"] = out if code == 0 else "None"

    # Working tree status
    code, out, _ = run_cmd(["git", "status", "--short"], cwd=project_root)
    telemetry["status"] = out if code == 0 and out else "Clean (no uncommitted changes)"

    # Diff stats
    code, out, _ = run_cmd(["git", "diff", "--stat"], cwd=project_root)
    telemetry["diff_stat"] = out if code == 0 and out else "No unstaged diffs"

    # Cached diff stats
    code, out, _ = run_cmd(["git", "diff", "--cached", "--stat"], cwd=project_root)
    telemetry["cached_diff_stat"] = out if code == 0 and out else "No staged diffs"

    # Detailed diff (truncated to 200 lines if too large)
    code, out, _ = run_cmd(["git", "diff"], cwd=project_root)
    if code == 0 and out:
        lines = out.splitlines()
        if len(lines) > 200:
            truncated_msg = f"\n... [Truncated: {len(lines) - 200} more lines]"
            telemetry["diff_sample"] = "\n".join(lines[:200]) + truncated_msg
        else:
            telemetry["diff_sample"] = out
    else:
        telemetry["diff_sample"] = "No active unstaged diffs."

    return telemetry


def get_test_telemetry(project_root: Path, run_tests: bool = False) -> str:
    """Check pytest status if requested, or report verified baseline."""
    if not run_tests:
        return (
            "Not re-executed (Baseline: 22 tests passing with strict "
            "Pydantic v2 / Hypothesis boundary validations)."
        )

    pytest_bin = project_root / ".venv" / "Scripts" / "pytest.exe"
    if not pytest_bin.exists():
        pytest_bin = Path("pytest")

    code, out, err = run_cmd([str(pytest_bin), "--tb=short", "-q"], cwd=project_root)
    combined = (out + "\n" + err).strip()
    status_str = "PASSED" if code == 0 else f"FAILED (exit code {code})"
    return f"{status_str}\n{combined}"


def copy_to_clipboard(text: str) -> bool:
    """Attempt to copy text to Windows clipboard."""
    try:
        proc = subprocess.Popen(
            ["clip.exe"],
            stdin=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        proc.communicate(input=text)
        return proc.returncode == 0
    except Exception:
        pass

    try:
        run_cmd(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"Set-Clipboard -Value @'\n{text}\n'@",
            ]
        )
        return True
    except Exception:
        return False


CORE_ARCHITECTURAL_INVARIANTS = """
### Non-Negotiable Biological & Technical Invariants (EthoPipe Standard)
1. **Mechanistic Determinism**: All models MUST utilize Pydantic v2 schemas
   configured with strict type validation (`ConfigDict(strict=True)`).
2. **Physiological Boundaries**: Canine heart rates MUST remain strictly clamped
   between `30` and `250` BPM (Toy: `80-200` BPM; Giant: `40-110` BPM).
3. **Darwin Core (DwC) Standardization**: All behavioral observation events MUST map
   onto Darwin Core `MeasurementOrFact` (`dwc:individualID`, `dwc:eventDate`,
   `dwc:measurementType`, `dwc:measurementValue`, `dwc:basisOfRecord`).
4. **Linguistic De-biasing**: Extraction pipelines MUST scrub anthropomorphic,
   subjective terms ('stubborn', 'spiteful', 'angry') and retain objective postures.
5. **Quality Benchmarks**: Code must pass `ruff format`, `ruff check`, `mypy`, and
   `pytest`.
""".strip()


def build_markdown_report(
    timestamp: str,
    objective: str,
    completed: str,
    in_progress: str,
    next_steps: str,
    blockers: str,
    notes: str,
    target_agent: str,
    telemetry: dict[str, str],
    test_status: str,
) -> str:
    """Build the comprehensive Markdown handoff report."""
    return f"""# EthoPipe Agent Handoff & Catch-Up Report

**Generated:** {timestamp}
**Active Branch:** `{telemetry["branch"]}`
**Target Agent / Model Profile:** `{target_agent}`

---

## 1. Executive Summary & Objective

- **Current Micro-Objective:** {objective}
- **Target Incoming Agent:** {target_agent}
- **Session Status:** Transitioning / Handoff

---

## 2. In-Flight Task Telemetry

### What Was Accomplished:
{completed}

### What Is Currently In-Progress / Uncommitted:
{in_progress}

### Immediate Next Steps for Incoming Agent:
{next_steps}

### Known Blockers, Edge-Cases & Warnings:
{blockers}

### Special Notes & Directives:
{notes}

---

## 3. Git Workspace Telemetry

- **Latest Commit:** `{telemetry["latest_commit"]}`
- **Working Tree Status (`git status --short`):**
```text
{telemetry["status"]}
```

- **Unstaged Diffs (`git diff --stat`):**
```text
{telemetry["diff_stat"]}
```

- **Staged Diffs (`git diff --cached --stat`):**
```text
{telemetry["cached_diff_stat"]}
```

- **Recent Commit History (`git log -n 5 --oneline`):**
```text
{telemetry["recent_commits"]}
```

---

## 4. Test & Verification Baseline

- **Test Suite Telemetry:**
```text
{test_status}
```

---

## 5. Architectural & Domain Invariants

{CORE_ARCHITECTURAL_INVARIANTS}

---

## 6. Key File & Context Map

- **Full Codebase Snapshot:** `docs/LLM_SNAPSHOT.md` (Concatenated repo sources)
- **Data Models:** `src/pipeline/models.py` (Pydantic v2 strict models)
- **Extraction / NLP:** `src/pipeline/parser.py` (Behavioral syllables & de-biasing)
- **API & Pipeline:** `src/pipeline/api.py`, `src/pipeline/main.py`
- **Testing Suite:** `tests/test_models.py`, `tests/test_api.py`
- **Automated QA Script:** `scripts/run_qa.ps1`
- **AI Governance Policy:** `docs/ai-usage.md`

---

*This report is auto-generated by `scripts/generate_agent_handoff.py`.*
"""


def build_catchup_prompt(
    timestamp: str,
    objective: str,
    completed: str,
    in_progress: str,
    next_steps: str,
    blockers: str,
    notes: str,
    target_agent: str,
    telemetry: dict[str, str],
    test_status: str,
) -> str:
    """Build the clean copy-pasteable prompt block for an incoming LLM agent."""
    diff_snippet = telemetry.get("diff_sample", "No active diffs.")
    if len(diff_snippet) > 1500:
        diff_snippet = (
            diff_snippet[:1500]
            + "\n... [diff truncated for prompt brevity, see docs/AGENT_HANDOFF.md]"
        )

    test_first_line = test_status.splitlines()[0] if test_status else "Passing"

    sep = "=" * 80
    return f"""{sep}
AGENT CATCH-UP & HANDOFF PROMPT (PASTE THIS INTO NEW MODEL / AGENT CHAT)
{sep}

<CONTEXT_HANDOFF>
# Role & Operational Persona
You are an expert Research Software Engineer (RSE) on the **EthoPipe** project.
EthoPipe is a deterministic, open-science Python ETL pipeline for canine ethology.
You are picking up work immediately from a previous agent session.

# Non-Negotiable Domain & Architectural Invariants
1. Pydantic v2 strict: All schemas must have `model_config = ConfigDict(strict=True)`.
2. Physiological bounds: Canine heart rate strictly clamped [30, 250] BPM
   (Toy: 80-200 BPM; Giant: 40-110 BPM).
3. Darwin Core (DwC): Observations map to `MeasurementOrFact` with `dwc:individualID`,
   `dwc:eventDate` (ISO 8601), `dwc:measurementType`, `dwc:measurementValue`.
4. Linguistic de-biasing: Scrub subjective terms ('stubborn', 'angry') for motor acts.
5. All code must pass `ruff format`, `ruff check`, `mypy`, and `pytest`.

# Workspace State Telemetry
- Active Branch: {telemetry["branch"]}
- Latest Commit: {telemetry["latest_commit"]}
- Working Tree:
{telemetry["status"]}
- Test Baseline: {test_first_line}

# Recent Active Diffs (Summary)
{telemetry["diff_stat"]}

# Active Unstaged Diffs Sample
```diff
{diff_snippet}
```

# Current Task & Next Actions
- Immediate Micro-Objective: {objective}
- Work Just Completed:
{completed}
- Currently In-Progress:
{in_progress}
- NEXT ACTIONS FOR YOU TO TAKE IMMEDIATELY:
{next_steps}
- Known Warnings / Blockers:
{blockers}
- Specific Directives:
{notes}

# Reference Documentation in Workspace
- Codebase snapshot: docs/LLM_SNAPSHOT.md
- Full handoff report: docs/AGENT_HANDOFF.md
- Governance guidelines: docs/ai-usage.md
- QA runner: scripts/run_qa.ps1

Please confirm you have ingested this context and state your plan immediately.
</CONTEXT_HANDOFF>
{sep}
"""


def build_companion_brief(
    timestamp: str,
    objective: str,
    companion_type: str,
    target_files: list[str],
    next_steps: str,
    blockers: str,
    telemetry: dict[str, str],
    test_status: str,
) -> str:
    """Build a deterministic brief strictly tailored for companions like Jules."""
    pr_prefix_map = {
        "bolt": "⚡ Bolt",
        "sentinel": "🛡️ Sentinel",
        "test": "test",
        "feature": "feat",
        "refactor": "refactor",
    }
    pr_prefix = pr_prefix_map.get(companion_type.lower(), "feat")
    pr_title = f"{pr_prefix}: {objective}"

    allowed_files_formatted = (
        "\n".join([f"- `{f.strip()}`" for f in target_files])
        if target_files
        else "- `src/pipeline/models.py` (Default - specify exact files as needed)"
    )

    journal_instruction = ""
    if companion_type.lower() == "bolt":
        journal_instruction = """
### Mandatory Learning Journal Update (.jules/bolt.md)
Upon completing this optimization, you MUST append a learning entry to
`.jules/bolt.md`:
```markdown
## YYYY-MM-DD - <Topic>
**Learning:** <Quantitative profiling or architectural discovery>
**Action:** <Code change implemented (e.g. O(1) hash lookup, caching)>
```
"""
    elif companion_type.lower() == "sentinel":
        journal_instruction = """
### Mandatory Learning Journal Update (.jules/sentinel.md)
Upon completing this security hardening, you MUST append a learning entry to
`.jules/sentinel.md`:
```markdown
## YYYY-MM-DD - <Topic>
**Learning:** <Vulnerability, input length boundary, or DoS vector resolved>
**Action:** <Pydantic validation or sanitization rule enforced>
```
"""

    sep = "=" * 80
    return f"""{sep}
CODE COMPANION (JULES) TASK BRIEF (PASTE INTO GITHUB ISSUE / COMPANION PROMPT)
{sep}

# Task Brief: {pr_title}

**Target Companion:** Google Labs Jules (`@google-labs-jules[bot]`) / Companion
**Task Track:** `{companion_type.upper()}`
**Target Branch:** `{telemetry["branch"]}`
**Recommended PR Title:** `{pr_title}`

---

## 1. Primary Objective
{objective}

---

## 2. Strict Modification Boundaries (Scope Control)
You are STRICTLY constrained to modify ONLY the following files:
{allowed_files_formatted}

Do NOT modify project configuration files (`pyproject.toml`,
`.pre-commit-config.yaml`, CI workflows) unless specifically authorized.

---

## 3. Required Implementation Steps
{next_steps}

---

## 4. Inviolable Repository Invariants (Do Not Violate)
1. **Pydantic v2 Strict Mode**: All models must have
   `model_config = ConfigDict(strict=True)`.
2. **Canine Heart Rate Bounds**: Clamped strictly between 30 and 250 BPM
   (Toy: 80-200 BPM, Giant: 40-110 BPM).
3. **Darwin Core (DwC)**: Behavioral syllables map to `MeasurementOrFact`
   (`dwc:individualID`, `dwc:eventDate`, `dwc:measurementType`,
   `dwc:measurementValue`, `dwc:basisOfRecord`).
4. **Linguistic De-biasing**: Discard subjective labels ('stubborn', 'spiteful')
   in favor of objective motor postures.
5. **Zero Test Regressions**: Current baseline has 22 passing tests.

---

## 5. Mandatory Verification Commands
Before submitting your pull request, you MUST execute and pass:
```bash
pytest tests/ --tb=short -q
ruff format --check src tests
ruff check src tests
```
{journal_instruction}

---

## 6. Known Context & Warnings
{blockers}

*Reference Snapshot: `docs/LLM_SNAPSHOT.md` | Status: `docs/AGENT_HANDOFF.md`*
{sep}
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate EthoPipe Agent Handoff and Code Companion Task Briefs."
    )
    parser.add_argument(
        "--objective",
        default="Standardizing project quality workflows and agent switching",
        help="Immediate micro-objective or goal for the incoming agent",
    )
    parser.add_argument(
        "--completed",
        default="- Verified pytest test baseline (22 passing tests)\n"
        "- Established workspace telemetry verification gates",
        help="Summary of work completed in the current session",
    )
    parser.add_argument(
        "--in-progress",
        default="Agent transition / handoff workflow setup and validation",
        help="Tasks currently in flight or uncommitted",
    )
    parser.add_argument(
        "--next-steps",
        default="1. Inspect working tree status\n"
        "2. Continue with assigned feature/bugfix objective\n"
        "3. Run tests via pytest",
        help="Immediate next steps for the incoming agent",
    )
    parser.add_argument(
        "--blockers",
        default="None. All baselines verified and passing.",
        help="Known blockers, pitfalls, or warnings",
    )
    parser.add_argument(
        "--notes",
        default="Targeting seamless cross-agent switching between paid models.",
        help="Additional instructions or directives",
    )
    parser.add_argument(
        "--target-agent",
        default="Any (Claude Code / OpenAI o1/4o / Cursor / Antigravity)",
        help="Designated incoming model/agent family (e.g. 'jules', 'claude')",
    )
    parser.add_argument(
        "--companion",
        action="store_true",
        help="Generate a specialized autonomous task brief for Jules / code companions",
    )
    parser.add_argument(
        "--companion-type",
        choices=["bolt", "sentinel", "test", "feature", "refactor"],
        default="bolt",
        help="Companion track: bolt (perf), sentinel (security), test, feature",
    )
    parser.add_argument(
        "--target-files",
        default="src/pipeline/models.py,tests/test_models.py",
        help="Comma-separated list of files the companion is permitted to modify",
    )
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Execute pytest to record real-time test telemetry in the report",
    )
    parser.add_argument(
        "--update-snapshot",
        action="store_true",
        help="Re-compile docs/LLM_SNAPSHOT.md via scripts/compile_snapshot.py",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Automatically copy the generated catch-up prompt to clipboard",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent

    # Optional: update snapshot
    if args.update_snapshot:
        snapshot_script = project_root / "scripts" / "compile_snapshot.py"
        if snapshot_script.exists():
            print("[+] Updating LLM Codebase Snapshot (docs/LLM_SNAPSHOT.md)...")
            run_cmd([sys.executable, str(snapshot_script)], cwd=project_root)

    # Gather telemetry
    print("[+] Gathering Git Telemetry...")
    telemetry = get_git_telemetry(project_root)

    print("[+] Gathering Test Suite Telemetry...")
    test_status = get_test_telemetry(project_root, run_tests=args.run_tests)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    is_companion = args.companion or args.target_agent.lower() in [
        "jules",
        "companion",
        "code-companion",
    ]

    target_file_list = [f.strip() for f in args.target_files.split(",") if f.strip()]

    # Generate documents
    report_md = build_markdown_report(
        timestamp=timestamp,
        objective=args.objective,
        completed=args.completed,
        in_progress=args.in_progress,
        next_steps=args.next_steps,
        blockers=args.blockers,
        notes=args.notes,
        target_agent="Google Labs Jules" if is_companion else args.target_agent,
        telemetry=telemetry,
        test_status=test_status,
    )

    if is_companion:
        prompt_text = build_companion_brief(
            timestamp=timestamp,
            objective=args.objective,
            companion_type=args.companion_type,
            target_files=target_file_list,
            next_steps=args.next_steps,
            blockers=args.blockers,
            telemetry=telemetry,
            test_status=test_status,
        )
    else:
        prompt_text = build_catchup_prompt(
            timestamp=timestamp,
            objective=args.objective,
            completed=args.completed,
            in_progress=args.in_progress,
            next_steps=args.next_steps,
            blockers=args.blockers,
            notes=args.notes,
            target_agent=args.target_agent,
            telemetry=telemetry,
            test_status=test_status,
        )

    # Save to docs/AGENT_HANDOFF.md
    docs_dir = project_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = docs_dir / "AGENT_HANDOFF.md"
    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[✓] Primary Handoff Report written to: {handoff_path}")

    # If companion, save to docs/JULES_TASK.md
    if is_companion:
        jules_task_path = docs_dir / "JULES_TASK.md"
        with open(jules_task_path, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        print(f"[✓] Code Companion Task Brief written to: {jules_task_path}")

    # Save historical archive to docs/handoffs/HANDOFF_<timestamp>.md
    archive_dir = docs_dir / "handoffs"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"HANDOFF_{file_timestamp}.md"
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[✓] Archived Handoff Report saved to: {archive_path}")

    # Clipboard support
    if args.copy:
        clipboard_copied = copy_to_clipboard(prompt_text)
        if clipboard_copied:
            print("[✓] Task Prompt successfully COPIED to Windows clipboard!")
        else:
            print("[!] Could not access clipboard. Please copy manually below.")

    # Print catchup prompt
    print("\n" + prompt_text)
    print(
        "\n[INFO] Workflow generated successfully.\n"
        "       Paste the prompt above into your target agent or GitHub issue.\n"
    )


if __name__ == "__main__":
    main()
