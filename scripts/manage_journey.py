#!/usr/bin/env python3
"""
EthoPipe Research Software Engineering Journey Manager

CLI utility to query, format, and append chronological logs and AI cognitive evolution
telemetry to JOURNEY.md without friction.
"""

from __future__ import annotations

import argparse
import datetime
import re
from pathlib import Path

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

TEMPLATE = """### Entry {entry_num}: {title}
* **Date & Model:** {date} | {model} | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** {hurdle}
* **The Technical Challenge:** {challenge}
* **AI Architectural Reasoning & Cognitive Evolution:**
  {reasoning}
* **The Architectural Pivot & Implemented Solution:**
  {pivot}
* **Quantitative & Invariant Milestones:** {milestone}
* **Gemini / AI Evolutionary Note:**
  {ai_note}
"""


class JourneyManager:
    def __init__(self, root: Path):
        self.root = root
        self.journey_file = root / "JOURNEY.md"

    def _read_journey(self) -> str:
        if not self.journey_file.exists():
            return ""
        return self.journey_file.read_text(encoding="utf-8")

    def get_next_entry_number(self) -> int:
        content = self._read_journey()
        entries = re.findall(r"### Entry (\d+):", content)
        if not entries:
            return 1
        return max(int(num) for num in entries) + 1

    def list_entries(self) -> list[dict[str, str]]:
        content = self._read_journey()
        pattern = re.compile(
            r"### Entry (\d+): ([^\n]+)\n\* \*\*Date & Model:\*\* ([^\n|]+) \| ([^\n|]+)",
            re.MULTILINE,
        )
        matches = []
        for m in pattern.finditer(content):
            matches.append(
                {
                    "entry": f"Entry {int(m.group(1)):03d}",
                    "title": m.group(2).strip(),
                    "date": m.group(3).strip(),
                    "model": m.group(4).strip(),
                }
            )
        return matches

    def generate_template(
        self, title: str = "Title of Milestone", model: str = "Gemini 3.8 Flash"
    ) -> str:
        next_num = f"{self.get_next_entry_number():03d}"
        today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
        return TEMPLATE.format(
            entry_num=next_num,
            title=title,
            date=today,
            model=model,
            hurdle="[Hurdle Category: Environmental / Architectural / Ingestion / Governance]",
            challenge="[Specific technical friction or anti-pattern encountered]",
            reasoning="[Detailed record of how the AI reasoned through the problem: trade-offs, constraints, alternative designs, and self-corrections]",
            pivot="[Key architectural changes, new abstractions, decoupled modules, or eliminated dependencies]",
            milestone="[Verified metrics: test counts, execution time, zero-bloat adherence, and passing audits]",
            ai_note="[Observations on AI model capabilities, reasoning fidelity, long-context handling, and human-AI synergy evolution]",
        )

    def append_entry(
        self,
        title: str,
        hurdle: str,
        challenge: str,
        reasoning: str,
        pivot: str,
        milestone: str,
        ai_note: str,
        model: str = "Gemini 3.8 Flash",
    ) -> str:
        content = self._read_journey()
        next_num = f"{self.get_next_entry_number():03d}"
        today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

        formatted_entry = TEMPLATE.format(
            entry_num=next_num,
            title=title,
            date=today,
            model=model,
            hurdle=hurdle,
            challenge=challenge,
            reasoning=reasoning.strip(),
            pivot=pivot.strip(),
            milestone=milestone.strip(),
            ai_note=ai_note.strip(),
        )

        # Insert before "## 🚀 Active Trajectory" or at the end of chronological logs
        marker = "## 🚀 Active Trajectory & Next Micro-Tasks"
        if marker in content:
            parts = content.split(marker)
            new_content = (
                parts[0].rstrip()
                + "\n\n"
                + formatted_entry
                + "\n---\n\n"
                + marker
                + parts[1]
            )
        else:
            new_content = content.rstrip() + "\n\n" + formatted_entry + "\n"

        self.journey_file.write_text(new_content, encoding="utf-8")
        return f"Entry {next_num}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="EthoPipe Journey & AI Evolution Manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all recorded Journey entries")

    # template
    tpl_parser = subparsers.add_parser(
        "template", help="Output blank entry template for session closing"
    )
    tpl_parser.add_argument(
        "--title", default="Milestone Title", help="Title for the draft entry"
    )
    tpl_parser.add_argument(
        "--model", default="Gemini 3.8 Flash", help="Active AI model"
    )

    # timeline
    subparsers.add_parser(
        "timeline", help="Display AI and architecture evolution timeline"
    )

    # new
    new_parser = subparsers.add_parser("new", help="Append a new entry to JOURNEY.md")
    new_parser.add_argument("--title", required=True, help="Milestone title")
    new_parser.add_argument(
        "--hurdle", required=True, help="Hurdle and problem classification"
    )
    new_parser.add_argument(
        "--challenge", required=True, help="The technical challenge"
    )
    new_parser.add_argument(
        "--reasoning",
        required=True,
        help="AI architectural reasoning and thought process",
    )
    new_parser.add_argument(
        "--pivot", required=True, help="Architectural pivot and solution"
    )
    new_parser.add_argument(
        "--milestone", required=True, help="Quantitative metrics and verification"
    )
    new_parser.add_argument(
        "--ai-note", required=True, help="AI evolutionary reflection note"
    )
    new_parser.add_argument(
        "--model", default="Gemini 3.8 Flash", help="Active AI model name"
    )

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    mgr = JourneyManager(root)

    if args.command == "list":
        entries = mgr.list_entries()
        print(
            f"\n{BOLD}{CYAN}=== EthoPipe Journey Chronicles & AI Evolution ==={RESET}\n"
        )
        if not entries:
            print("No parsed entries found.")
            return
        for e in entries:
            print(f"  {GREEN}{e['entry']}{RESET}: {BOLD}{e['title']}{RESET}")
            print(f"           Date: {e['date']} | Model: {YELLOW}{e['model']}{RESET}")
        print(f"\nTotal Entries: {len(entries)}\n")

    elif args.command == "template":
        print(mgr.generate_template(title=args.title, model=args.model))

    elif args.command == "timeline":
        print(
            f"\n{BOLD}{CYAN}=== EthoPipe AI Co-Evolution Trajectory (2025 - 2026+) ==={RESET}\n"
        )
        print("  • 2025 - Initial Foundation & Heuristics (Gemini 1.5 Pro / Flash)")
        print(
            "    - Focus: Pydantic schemas, initial Darwin Core biological constraints, Docker setup."
        )
        print("    - Paradigm: Reactive code generation, basic prompt instructions.")
        print("  • Mid 2026 - Radical Determinism & Verification (Gemini 3.5 Flash)")
        print(
            "    - Focus: Property-based testing (Hypothesis), pre-commit gates, credential isolation."
        )
        print(
            "    - Paradigm: Deterministic guardrails, zero-variance temperature, strict type safety."
        )
        print(
            "  • Late 2026 - Autonomous Governance & Meta-Cognition (Gemini 3.8 Flash)"
        )
        print(
            "    - Focus: Solo maintainer anti-bloat charter, step-gated idea engine, telemetry handoff."
        )
        print(
            "    - Paradigm: Proactive systems architecture, AI cognitive journaling, automated governance.\n"
        )

    elif args.command == "new":
        entry_tag = mgr.append_entry(
            title=args.title,
            hurdle=args.hurdle,
            challenge=args.challenge,
            reasoning=args.reasoning,
            pivot=args.pivot,
            milestone=args.milestone,
            ai_note=args.ai_note,
            model=args.model,
        )
        print(f"{GREEN}[✓] Successfully appended {entry_tag} to JOURNEY.md{RESET}")


if __name__ == "__main__":
    main()
