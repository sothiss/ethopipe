#!/usr/bin/env python3
"""EthoPipe Project Goals & State Management Engine.

Provides an authoritative, frictionless mechanism to track:
1. Current Project Goals (Immediate, Near-Term, Long-Term Roadmap).
2. Live Working State (What is done, what is active, where work stopped).
3. Immediate Quick-Resume Instructions (How to pick up seamlessly).
4. Immutable Dated History Snapshots (docs/states/STATE_YYYYMMDD_HHMMSS.md).
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

DEFAULT_PHASE = "Phase 4 (JOSS Publication, Zenodo Minting & Architectural Hardening)"


def get_git_telemetry(root: Path) -> dict[str, str]:
    """Extract current git branch, commit hash, and working tree status."""
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=str(root),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        branch = "main"

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(root),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        commit = "unknown"

    try:
        status_lines = (
            subprocess.check_output(
                ["git", "status", "--short"],
                cwd=str(root),
                text=True,
                stderr=subprocess.DEVNULL,
            )
            .strip()
            .splitlines()
        )
        dirty_count = len(status_lines)
    except Exception:
        dirty_count = 0

    return {
        "branch": branch or "main",
        "commit": commit,
        "dirty_count": str(dirty_count),
    }


class ProjectStateManager:
    def __init__(self, root: Path):
        self.root = root
        self.docs_dir = root / "docs"
        self.state_file = self.docs_dir / "PROJECT_STATE.md"
        self.history_dir = self.docs_dir / "states"
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def load_current_state(self) -> str:
        """Load the active PROJECT_STATE.md file if present."""
        if not self.state_file.exists():
            return ""
        return self.state_file.read_text(encoding="utf-8")

    def print_status(self) -> None:
        """Pretty-print current goals, stopping point, and next steps."""
        if not self.state_file.exists():
            msg = "[!] No PROJECT_STATE.md found. Run 'checkpoint' to create one."
            print(f"{YELLOW}{msg}{RESET}")
            return

        content = self.load_current_state()
        print(f"\n{BOLD}{CYAN}{'═' * 64}{RESET}")
        print(f"{BOLD}{CYAN}   EthoPipe Live Project State & Goals{RESET}")
        print(f"{BOLD}{CYAN}{'═' * 64}{RESET}\n")

        phase_m = re.search(r"\*\*Current Phase:\*\*\s*(.+)", content)
        focus_m = re.search(r"\*\*Active Focus:\*\*\s*(.+)", content)
        stopped_m = re.search(
            r"### 📍 Where We Stopped\n(.*?)(?=\n###|\n---|\Z)", content, re.DOTALL
        )
        next_m = re.search(
            r"### 🚀 Quick-Resume Action\n(.*?)(?=\n###|\n---|\Z)", content, re.DOTALL
        )
        goals_m = re.search(
            r"## 🎯 Project Goals Roadmap\n(.*?)(?=\n## 🛡️|\n---|\Z)",
            content,
            re.DOTALL,
        )

        if phase_m:
            print(f"{BOLD}Phase:{RESET}        {phase_m.group(1).strip()}")
        if focus_m:
            print(f"{BOLD}Active Focus:{RESET} {focus_m.group(1).strip()}")

        if stopped_m:
            print(f"\n{BOLD}{YELLOW}📍 Stopping Point / Current State:{RESET}")
            for line in stopped_m.group(1).strip().splitlines()[:6]:
                print(f"   {line}")

        if next_m:
            print(f"\n{BOLD}{GREEN}🚀 Quick-Resume Next Action:{RESET}")
            for line in next_m.group(1).strip().splitlines()[:6]:
                print(f"   {line}")

        if goals_m:
            print(f"\n{BOLD}{CYAN}🎯 Goals Summary:{RESET}")
            for line in goals_m.group(1).strip().splitlines()[:15]:
                stripped = line.strip()
                if stripped.startswith("- [") or stripped.startswith("###"):
                    print(f"   {stripped}")

        print(f"\n{BOLD}{'═' * 64}{RESET}")
        print(f"Full details: {CYAN}{self.state_file}{RESET}\n")

    def list_history(self) -> None:
        """List historical checkpoint snapshots in docs/states/."""
        checkpoints = sorted(
            self.history_dir.glob("STATE_*.md"),
            reverse=True,
        )
        print(f"\n{BOLD}{CYAN}{'═' * 64}{RESET}")
        title = f"   EthoPipe Historical State Checkpoints ({len(checkpoints)})"
        print(f"{BOLD}{CYAN}{title}{RESET}")
        print(f"{BOLD}{CYAN}{'═' * 64}{RESET}\n")

        if not checkpoints:
            msg = f"No historical checkpoints found in {self.history_dir}"
            print(f"{YELLOW}{msg}{RESET}\n")
            return

        for cp in checkpoints:
            text = cp.read_text(encoding="utf-8")
            date_m = re.search(r"\*\*Updated:\*\*\s*`([^`]+)`", text)
            focus_m = re.search(r"\*\*Active Focus:\*\*\s*([^\n]+)", text)
            stopped_m = re.search(r"### 📍 Where We Stopped\n([^\n]+)", text)

            date_str = date_m.group(1) if date_m else cp.stem.replace("STATE_", "")
            focus_str = focus_m.group(1).strip() if focus_m else "Checkpoint"
            stopped_str = stopped_m.group(1).strip() if stopped_m else ""

            print(f"{GREEN}[●] {cp.name}{RESET}")
            print(f"    Date:   {date_str}")
            print(f"    Focus:  {focus_str}")
            if stopped_str:
                print(f"    State:  {stopped_str[:90]}")
            print()

        print(f"{BOLD}{'═' * 64}{RESET}\n")

    def create_checkpoint(
        self,
        focus: str,
        stopped_at: str,
        next_step: str,
        immediate_goals: list[str] | None = None,
        near_term_goals: list[str] | None = None,
        long_term_goals: list[str] | None = None,
        phase: str = DEFAULT_PHASE,
    ) -> Path:
        """Update docs/PROJECT_STATE.md and archive a dated copy in docs/states/."""
        now_dt = datetime.datetime.now(datetime.UTC)
        timestamp_display = now_dt.strftime("%Y-%m-%d %H:%M:%SZ")
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        git_meta = get_git_telemetry(self.root)
        branch = git_meta["branch"]
        commit = git_meta["commit"]
        dirty = git_meta["dirty_count"]

        imm = immediate_goals or [
            "[x] Strict Solo Maintainer Audit verification (100% clean, 8/8 deps)",
            "[x] Historical audit snapshot archiving in docs/audits/",
            "[x] State & Goals checkpointing workflow implementation",
            "[ ] Localized storage adapter for Star Schema persistence",
            "[ ] Direct Google AI Studio response schema validation binding",
        ]
        near = near_term_goals or [
            "[ ] JOSS manuscript preparation (`paper.md`, `paper.bib`)",
            "[ ] Supabase PostgreSQL real-time replication endpoint hardening",
            "[ ] Automated end-to-end stress test for multi-dog ingestion",
        ]
        long_term = long_term_goals or [
            "[ ] Zenodo DOI citation indexing in biodiversity databases",
            "[ ] Global Darwin Core (DwC) Archive export automation",
            "[ ] Deployment of The Transparency Project public telemetry portal",
        ]

        md = [
            "# EthoPipe Project Goals & Active State",
            "",
            f"**Last Updated:** `{timestamp_display}`",
            f"**Current Phase:** {phase}",
            f"**Active Focus:** {focus}",
            f"**Active Branch:** `{branch}` (`{commit}` | Dirty: {dirty})",
            "",
            "---",
            "",
            "## 📍 Current Stopping Point & Where to Resume",
            "",
            "### 📍 Where We Stopped",
            stopped_at.strip(),
            "",
            "### 🚀 Quick-Resume Action",
            next_step.strip(),
            "",
            "---",
            "",
            "## 🎯 Project Goals Roadmap",
            "",
            "### 1. Immediate Session Goals (Current Sprint)",
        ]
        for g in imm:
            md.append(f"- {g if g.startswith('[') else '[ ] ' + g}")

        md.extend(
            [
                "",
                "### 2. Near-Term Goals (Next Milestones)",
            ]
        )
        for g in near:
            md.append(f"- {g if g.startswith('[') else '[ ] ' + g}")

        md.extend(
            [
                "",
                "### 3. Long-Term Architectural Milestones",
            ]
        )
        for g in long_term:
            md.append(f"- {g if g.startswith('[') else '[ ] ' + g}")

        md.extend(
            [
                "",
                "---",
                "",
                "## 🛡️ Repository Invariants & Guardrails",
                "- **Language Monoculture**: 100% Python (no Node, Rust, Go).",
                "- **Dependency Budget**: Max 8 runtime packages (Currently 8/8).",
                "- **Prohibited Daemons**: Zero external brokers (Redis, Celery).",
                "- **Biological Bounds**: Canine HR clamped [30, 250] BPM.",
                "- **Biodiversity Interop**: Darwin Core (`MeasurementOrFact`).",
                "- **Test Baseline**: 27 tests passing with >= 90% coverage.",
                "",
                "---",
                (
                    "*Auto-generated and managed via `scripts/manage_project_state.py` "
                    "and `scripts/state.ps1`.*"
                ),
            ]
        )

        full_content = "\n".join(md) + "\n"

        # 1. Update live document
        self.state_file.write_text(full_content, encoding="utf-8")
        print(f"{GREEN}[✓] Active state updated: {self.state_file}{RESET}")

        # 2. Archive dated copy
        archive_file = self.history_dir / f"STATE_{file_timestamp}.md"
        archive_file.write_text(full_content, encoding="utf-8")
        print(f"{CYAN}[✓] Historical checkpoint saved: {archive_file}{RESET}")

        return archive_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="EthoPipe Project Goals & State Management Utility."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser(
        "status", help="Print current project state and quick-resume step."
    )
    subparsers.add_parser("history", help="List all historical checkpoints.")

    cp_parser = subparsers.add_parser(
        "checkpoint", help="Record a new project state checkpoint."
    )
    cp_parser.add_argument(
        "--focus", required=True, help="Current focus / milestone title."
    )
    cp_parser.add_argument(
        "--stopped-at", required=True, help="Description of where work was paused."
    )
    cp_parser.add_argument(
        "--next-step", required=True, help="Immediate next action to resume work."
    )
    cp_parser.add_argument(
        "--phase",
        default=DEFAULT_PHASE,
        help="Current project phase.",
    )
    cp_parser.add_argument(
        "--goal",
        action="append",
        dest="goals",
        help="Immediate goal item (can repeat).",
    )

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    mgr = ProjectStateManager(root)

    if args.command in (None, "status"):
        mgr.print_status()
        return 0

    if args.command == "history":
        mgr.list_history()
        return 0

    if args.command == "checkpoint":
        mgr.create_checkpoint(
            focus=args.focus,
            stopped_at=args.stopped_at,
            next_step=args.next_step,
            phase=args.phase,
            immediate_goals=args.goals,
        )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
