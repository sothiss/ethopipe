#!/usr/bin/env python3
"""
EthoPipe Research Software Engineering Journey & Walkthrough Archive Manager

CLI utility to query, format, archive session Task/Walkthrough artifacts into
docs/walkthroughs/, and append chronological AI evolution logs to JOURNEY.md.
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
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
  {ai_note}{walkthrough_line}
"""


def get_git_summary(root: Path) -> str:
    """Return 'branch @ short_sha' for metadata provenance."""
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=str(root),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(root),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return f"{branch or 'main'} @ {sha}"
    except Exception:
        return "main"


class JourneyManager:
    def __init__(self, root: Path):
        self.root = root
        self.journey_file = root / "JOURNEY.md"
        self.walkthroughs_dir = root / "docs" / "walkthroughs"
        self.walkthroughs_dir.mkdir(parents=True, exist_ok=True)

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
        regex_pattern = (
            r"### Entry (\d+): ([^\n]+)\n"
            r"\* \*\*Date & Model:\*\* ([^\n|]+) \| ([^\n|]+)"
        )
        pattern = re.compile(regex_pattern, re.MULTILINE)
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

    def list_walkthroughs(self) -> list[dict[str, str]]:
        archives = sorted(
            self.walkthroughs_dir.glob("WALKTHROUGH_*.md"),
            reverse=True,
        )
        items: list[dict[str, str]] = []
        for path in archives:
            text = path.read_text(encoding="utf-8", errors="replace")
            title_m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            model_m = re.search(r"\*\*Model & Harness:\*\*\s*`([^`]+)`", text)
            date_m = re.search(r"\*\*Archived:\*\*\s*`([^`]+)`", text)
            items.append(
                {
                    "file": path.name,
                    "title": title_m.group(1).strip() if title_m else path.stem,
                    "model": model_m.group(1).strip() if model_m else "Unknown",
                    "date": date_m.group(1).strip() if date_m else "",
                }
            )
        return items

    def archive_walkthrough(
        self,
        title: str,
        model: str,
        ide: str = "Google Antigravity IDE",
        task_file: Path | None = None,
        walkthrough_file: Path | None = None,
    ) -> Path:
        """Persist a dated Task + Walkthrough snapshot inside docs/walkthroughs/."""
        now_utc = datetime.datetime.now(datetime.UTC)
        iso_ts = now_utc.strftime("%Y-%m-%d %H:%M:%SZ")
        file_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48]
        out_path = self.walkthroughs_dir / f"WALKTHROUGH_{file_ts}_{slug}.md"

        git_ref = get_git_summary(self.root)
        task_md = (
            task_file.read_text(encoding="utf-8").strip()
            if task_file and task_file.exists()
            else "_No separate task checklist provided._"
        )
        walkthrough_md = (
            walkthrough_file.read_text(encoding="utf-8").strip()
            if walkthrough_file and walkthrough_file.exists()
            else "_No separate walkthrough file provided._"
        )

        # Normalize machine-local file:/// links pointing inside this workspace
        # into clean repo-relative links so they work everywhere on GitHub.
        root_uri = self.root.resolve().as_posix()
        root_uri_enc = root_uri.replace(" ", "%20")
        for prefix in (f"file:///{root_uri_enc}/", f"file:///{root_uri}/"):
            task_md = task_md.replace(prefix, "../../")
            walkthrough_md = walkthrough_md.replace(prefix, "../../")

        doc = f"""# Session Archive: {title}

* **Archived:** `{iso_ts}`
* **Model & Harness:** `{model} ({ide})`
* **Human PI:** Alice Severi Gonçalves (`@sothiss`)
* **Git Provenance:** `{git_ref}`

---

## Part I — Up-Front & Finalized Task Checklist

{task_md}

---

## Part II — Post-Execution Walkthrough & AI Reasoning

{walkthrough_md}
"""
        out_path.write_text(doc, encoding="utf-8")
        return out_path

    def generate_template(
        self, title: str = "Title of Milestone", model: str = "Gemini 4 (Medium)"
    ) -> str:
        next_num = f"{self.get_next_entry_number():03d}"
        today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
        return TEMPLATE.format(
            entry_num=next_num,
            title=title,
            date=today,
            model=model,
            hurdle="[Environmental / Architecture / Ingestion / Governance]",
            challenge="[Specific technical friction or constraint encountered]",
            reasoning=(
                "[Detailed record of how the AI reasoned through the problem: "
                "trade-offs, constraints, alternative designs, and self-corrections]"
            ),
            pivot=(
                "[Key architectural changes, new abstractions, decoupled modules, "
                "or eliminated dependencies]"
            ),
            milestone=(
                "[Verified metrics: test counts, execution time, zero-bloat "
                "adherence, and passing audits]"
            ),
            ai_note=(
                "[Observations on AI model capabilities, reasoning fidelity, "
                "long-context handling, and human-AI synergy evolution]"
            ),
            walkthrough_line=(
                "\n* **Session Task & Walkthrough Archive:** "
                "`docs/walkthroughs/WALKTHROUGH_YYYYMMDD_HHMMSS_topic.md`"
            ),
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
        model: str = "Gemini 4 (Medium)",
        walkthrough_ref: str = "",
    ) -> str:
        content = self._read_journey()
        next_num = f"{self.get_next_entry_number():03d}"
        today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

        wt_line = ""
        if walkthrough_ref.strip():
            ref = walkthrough_ref.strip().replace("\\", "/")
            name = Path(ref).name
            wt_line = f"\n* **Session Task & Walkthrough Archive:** [{name}]({ref})"

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
            walkthrough_line=wt_line,
        )

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
        description="EthoPipe Journey & Walkthrough Archive Manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser(
        "list", help="List all recorded Journey entries and archived walkthroughs"
    )

    # template
    tpl_parser = subparsers.add_parser(
        "template", help="Output blank entry template for session closing"
    )
    tpl_parser.add_argument(
        "--title", default="Milestone Title", help="Title for the draft entry"
    )
    tpl_parser.add_argument(
        "--model", default="Gemini 4 (Medium)", help="Active AI model"
    )

    # timeline
    subparsers.add_parser(
        "timeline", help="Display AI and architecture evolution timeline"
    )

    # archive
    arc_parser = subparsers.add_parser(
        "archive",
        help="Archive session task.md and walkthrough.md into docs/walkthroughs/",
    )
    arc_parser.add_argument("--title", required=True, help="Session title")
    arc_parser.add_argument(
        "--model", default="Gemini 4 (Medium)", help="Human-readable model name"
    )
    arc_parser.add_argument(
        "--ide", default="Google Antigravity IDE", help="Agent IDE or harness"
    )
    arc_parser.add_argument("--task-file", help="Path to session task.md")
    arc_parser.add_argument("--walkthrough-file", help="Path to session walkthrough.md")

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
        "--model", default="Gemini 4 (Medium)", help="Active AI model name"
    )
    new_parser.add_argument(
        "--walkthrough-ref",
        default="",
        help="Repo-relative path to archived walkthrough in docs/walkthroughs/",
    )

    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    mgr = JourneyManager(root)

    if args.command == "list":
        entries = mgr.list_entries()
        print(
            f"\n{BOLD}{CYAN}=== EthoPipe Journey Chronicles & AI Evolution ==={RESET}\n"
        )
        for e in entries:
            print(f"  {GREEN}{e['entry']}{RESET}: {BOLD}{e['title']}{RESET}")
            print(f"           Date: {e['date']} | Model: {YELLOW}{e['model']}{RESET}")
        print(f"\nTotal Journey Entries: {len(entries)}")

        archives = mgr.list_walkthroughs()
        print(
            f"\n{BOLD}{CYAN}=== Archived Session Tasks & Walkthroughs "
            f"({len(archives)}) ==={RESET}\n"
        )
        if not archives:
            print("  No archived walkthroughs in docs/walkthroughs/ yet.\n")
        else:
            for a in archives:
                print(f"  {GREEN}[✓] {a['file']}{RESET}")
                print(f"      {a['title']} | {YELLOW}{a['model']}{RESET} | {a['date']}")
            print()

    elif args.command == "template":
        print(mgr.generate_template(title=args.title, model=args.model))

    elif args.command == "timeline":
        header = f"\n{BOLD}{CYAN}=== EthoPipe AI Co-Evolution Trajectory ==={RESET}\n"
        print(header)
        print(
            "  • Phase 0 (2025): Conceptualization, visual phenotyping & DB prototypes"
        )
        print(
            "  • Phase 1 (May 2026): 50-day sprint in Antigravity IDE (Gemini 3.1 Pro)"
        )
        print(
            "  • Phase 2 (June 2026): EthoPipe ETL, Temp 0.0 DwC & Pydantic v2 "
            "locking (Gemini 1.5 Pro)"
        )
        print(
            "  • Phase 3 (July-Aug 2026): Cloud Launchpad Fellowship & 1M context "
            "migration (Gemini 2.5 Pro)"
        )
        print(
            "  • Phase 4 (Aug-Oct 2026): Pivot to Gemini 3.5 Flash, 43-test "
            "baseline, Zenodo DOI & JOSS prep"
        )
        print(
            "  • Phase 5 (Late 2026): Solo Maintainer Charter, 5-Gate Ideas & "
            "Walkthrough Archives (Gemini 3.8 / Gemini 4)\n"
        )

    elif args.command == "archive":
        t_path = Path(args.task_file) if args.task_file else None
        w_path = Path(args.walkthrough_file) if args.walkthrough_file else None
        saved = mgr.archive_walkthrough(
            title=args.title,
            model=args.model,
            ide=args.ide,
            task_file=t_path,
            walkthrough_file=w_path,
        )
        rel = saved.relative_to(root).as_posix()
        print(f"{GREEN}[✓] Archived session Task & Walkthrough to: {rel}{RESET}")

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
            walkthrough_ref=args.walkthrough_ref,
        )
        print(f"{GREEN}[✓] Successfully appended {entry_tag} to JOURNEY.md{RESET}")


if __name__ == "__main__":
    main()
