#!/usr/bin/env python3
"""
EthoPipe Step-Gated Idea & Task Pipeline Engine

Prevents skipping steps when moving from Idea -> Specification -> Test -> Code -> Done.
Enforces the Solo Maintainer Charter and the 5-Gate Development Pipeline.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path
from typing import Any

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

TRACKS = ["bolt", "sentinel", "feat", "refactor", "docs"]
GATES = [
    "Gate 1: Triage & Solo Maintainer Veto",
    "Gate 2: Boundary Specification",
    "Gate 3: Adversarial Test First",
    "Gate 4: Minimal Implementation (KISS)",
    "Gate 5: QA & Journal Verification",
]


class IdeaManager:
    def __init__(self, root: Path):
        self.root = root
        self.ideas_dir = root / "docs" / "ideas"
        self.ideas_dir.mkdir(parents=True, exist_ok=True)

    def _next_id(self) -> str:
        existing = list(self.ideas_dir.glob("IDEA-*.md"))
        max_id = 0
        for p in existing:
            match = re.match(r"IDEA-(\d+)", p.name)
            if match:
                max_id = max(max_id, int(match.group(1)))
        return f"IDEA-{max_id + 1:03d}"

    def create_idea(self, title: str, track: str) -> Path:
        if track not in TRACKS:
            raise ValueError(f"Invalid track '{track}'. Choose from {TRACKS}")

        idea_id = self._next_id()
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        filename = f"{idea_id}_{slug}.md"
        file_path = self.ideas_dir / filename

        today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

        content = f"""# [{idea_id}] {title}

**Track:** `{track}` | **Created:** `{today}` | **Status:** `in-triage`  
**Current Gate:** `Gate 1: Triage & Solo Maintainer Veto`

---

## 🎯 Objective & Problem Statement
*Describe clearly what problem this solves and why it is needed.*

---

## 🛑 The 5 Non-Negotiable Gates (Do Not Skip Steps!)

### Gate 1: Triage & Solo Maintainer Veto
- [ ] **Language Monoculture**: 100% pure Python (no Node, npm, Rust, Go).
- [ ] **Dependency Check**: Uses stdlib or existing packages. Zero new dependencies.
- [ ] **Daemon Check**: Zero external message brokers (Redis, Celery, Airflow).
- [ ] **YAGNI / KISS**: Truly required now, not speculative over-engineering.

### Gate 2: Boundary Specification
- [ ] **Target Files**: List exact files to touch (e.g. `src/pipeline/models.py`).
- [ ] **Biological Bounds**: Heart rate clamped to [30, 250] BPM (if applicable).
- [ ] **Darwin Core**: Maps to DwC MeasurementOrFact attributes (if applicable).
- [ ] **Linguistic De-biasing**: Discards subjective labels (if applicable).

### Gate 3: Adversarial Test First
- [ ] **Failing Test Written**: Create or update test in `tests/` before implementation.
- [ ] **Boundary / Property Cases**: Hypothesis strategy or boundary cases defined.

### Gate 4: Minimal Implementation (KISS)
- [ ] **File Size Limit**: Target files remain strictly under 600 lines.
- [ ] **Strict Typing**: Pydantic models use `ConfigDict(strict=True)`.
- [ ] **No Dead Code**: Remove all debug statements and unused imports.

### Gate 5: QA & Journal Verification
- [ ] **All 8 Steps Pass**: Run `.\\scripts\\run_qa.ps1` with 0 failures.
- [ ] **Journal Updated**:
  - If `bolt`: Append learning entry to `.jules/bolt.md`.
  - If `sentinel`: Append defensive entry to `.jules/sentinel.md`.
  - If `feat` / `refactor`: Update `CHANGELOG.md`.

---

## 📝 Implementation Notes & Scratchpad
*Log commands, profiling data, or code snippets here during development.*
"""
        file_path.write_text(content, encoding="utf-8")
        self.update_board()
        return file_path

    def parse_ideas(self) -> list[dict[str, Any]]:
        ideas = []
        for file in sorted(self.ideas_dir.glob("IDEA-*.md")):
            text = file.read_text(encoding="utf-8", errors="replace")
            first_line = text.splitlines()[0] if text.splitlines() else ""
            match_id = re.match(r"#\s*\[(IDEA-\d+)\]\s*(.*)", first_line)
            idea_id = match_id.group(1) if match_id else file.stem
            title = match_id.group(2) if match_id else file.stem

            track_match = re.search(r"\*\*Track:\*\*\s*`([^`]+)`", text)
            track = track_match.group(1) if track_match else "unknown"

            status_match = re.search(r"\*\*Status:\*\*\s*`([^`]+)`", text)
            status = status_match.group(1) if status_match else "draft"

            gate_match = re.search(r"\*\*Current Gate:\*\*\s*`([^`]+)`", text)
            current_gate = gate_match.group(1) if gate_match else "Gate 1"

            # Count checked boxes
            total_checks = len(re.findall(r"- \[[ xX]\]", text))
            completed_checks = len(re.findall(r"- \[[xX]\]", text))

            ideas.append(
                {
                    "id": idea_id,
                    "title": title,
                    "track": track,
                    "status": status,
                    "current_gate": current_gate,
                    "completed_checks": completed_checks,
                    "total_checks": total_checks,
                    "file": file,
                    "text": text,
                }
            )
        return ideas

    def update_board(self) -> Path:
        board_path = self.root / "docs" / "IDEAS_BOARD.md"
        ideas = self.parse_ideas()
        now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%SZ")

        lines = [
            "# EthoPipe Idea & Task Board",
            "",
            f"**Last Synchronized:** `{now}`  ",
            "**Pipeline Status:** Active Step-Gated Anti-Skipping System",
            "",
            "## 📋 Active Tasks & Ideas",
            "",
            "| ID | Track | Title | Current Gate | Progress | File |",
            "| :--- | :---: | :--- | :--- | :---: | :--- |",
        ]

        if not ideas:
            lines.append("| - | - | *No active ideas registered.* | - | - | - |")
        else:
            for item in ideas:
                pct = (
                    int((item["completed_checks"] / item["total_checks"]) * 100)
                    if item["total_checks"] > 0
                    else 0
                )
                rel_path = item["file"].relative_to(self.root).as_posix()
                lines.append(
                    f"| **{item['id']}** | `{item['track']}` | "
                    f"{item['title']} | `{item['current_gate']}` | "
                    f"{item['completed_checks']}/{item['total_checks']} ({pct}%) | "
                    f"[{item['id']}]({rel_path}) |"
                )

        lines.extend(
            [
                "",
                "---",
                "",
                "## 🔒 The 5-Gate Sequence",
                "",
                "1. **Gate 1: Triage & Solo Maintainer Veto** "
                "— Language monoculture, dependency budget, and YAGNI.",
                "2. **Gate 2: Boundary Specification** "
                "— Target files, Darwin Core mapping, and physiological limits.",
                "3. **Gate 3: Adversarial Test First** "
                "— Writing the test/Hypothesis case *before* production code.",
                "4. **Gate 4: Minimal Implementation (KISS)** "
                "— Clean, strict Pydantic v2 under 600 lines.",
                "5. **Gate 5: QA & Journal Verification** "
                "— All 8 steps of `.\\scripts\\run_qa.ps1` + journal logging.",
                "",
                "### CLI Commands",
                "```powershell",
                "# Create a new idea",
                '.\\scripts\\idea.ps1 -New "My Idea" -Track bolt',
                "",
                "# Audit that no gates were skipped",
                "python scripts/manage_ideas.py audit",
                "```",
            ]
        )

        board_path.write_text("\n".join(lines), encoding="utf-8")
        return board_path

    def audit_ideas(self) -> bool:
        ideas = self.parse_ideas()
        all_compliant = True
        print(f"\n{BOLD}{CYAN}════════════════════════════════════════════════{RESET}")
        print(f"{BOLD}{CYAN}   EthoPipe Step-Skipping & Task Audit          {RESET}")
        print(f"{BOLD}{CYAN}════════════════════════════════════════════════{RESET}\n")

        for item in ideas:
            text = item["text"]
            is_done = "done" in item["status"].lower()
            unresolved_checks = len(re.findall(r"- \[ \]", text))

            # If marked done but has unresolved checks, that is a skipped step!
            if is_done and unresolved_checks > 0:
                all_compliant = False
                print(
                    f"  {RED}[✗] SKIPPED STEPS DETECTED:{RESET} {item['id']} "
                    f"'{item['title']}' is marked done with {unresolved_checks} "
                    f"unchecked gate(s)!"
                )
            else:
                pct = (
                    int((item["completed_checks"] / item["total_checks"]) * 100)
                    if item["total_checks"] > 0
                    else 0
                )
                title_preview = (
                    item["title"][:30] + "..."
                    if len(item["title"]) > 33
                    else item["title"]
                )
                print(
                    f"  {GREEN}[✓] VALIDATED:{RESET} {item['id']} "
                    f"[{item['track'].upper()}] - {title_preview} "
                    f"({item['completed_checks']}/{item['total_checks']}, {pct}%)"
                )

        print()
        if all_compliant:
            msg = "🎉 PASSED: Zero skipped steps across tracked ideas!"
            print(f"{GREEN}{BOLD}{msg}{RESET}\n")
        else:
            msg = "❌ AUDIT FAILED: Unresolved gates in completed tasks!"
            print(f"{RED}{BOLD}{msg}{RESET}\n")

        return all_compliant


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage EthoPipe ideas and enforce step-by-step gates."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # new command
    new_parser = subparsers.add_parser("new", help="Create a new step-gated idea")
    new_parser.add_argument("title", help="Descriptive title of the idea")
    new_parser.add_argument(
        "--track",
        choices=TRACKS,
        default="feat",
        help=f"Task typology track ({', '.join(TRACKS)})",
    )

    # list command
    subparsers.add_parser("list", help="List all ideas and progress")

    # audit command
    subparsers.add_parser("audit", help="Audit that no task skipped required gates")

    # board command
    subparsers.add_parser("board", help="Re-generate docs/IDEAS_BOARD.md")

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    manager = IdeaManager(root=root)

    if args.command == "new":
        path = manager.create_idea(title=args.title, track=args.track)
        print(f"{GREEN}[✓] Created step-gated idea file: {path.name}{RESET}")
        print(f"{CYAN}Open and complete Gate 1 before writing code!{RESET}")
        return 0

    elif args.command == "list":
        ideas = manager.parse_ideas()
        if not ideas:
            print("No ideas found in docs/ideas/.")
            return 0
        print(f"\n{'ID':<10} {'TRACK':<10} {'STATUS':<12} {'CHECKS':<8} {'TITLE'}")
        print("-" * 65)
        for i in ideas:
            checks = f"{i['completed_checks']}/{i['total_checks']}"
            title_str = i["title"][:28]
            print(
                f"{i['id']:<10} {i['track']:<10} {i['status']:<12} {checks:<8} "
                f"{title_str}"
            )
        print()
        return 0

    elif args.command == "audit":
        compliant = manager.audit_ideas()
        return 0 if compliant else 1

    elif args.command == "board":
        board = manager.update_board()
        print(f"{GREEN}[✓] Updated ideas board: {board}{RESET}")
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
