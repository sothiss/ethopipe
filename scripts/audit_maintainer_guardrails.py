#!/usr/bin/env python3
"""
EthoPipe Solo Maintainer Guardrails & Anti-Bloat Audit Engine

Audits repository health against the Solo Maintainer Charter:
1. Language Monoculture (Strict Python 3.11+, zero polyglot sprawl)
2. Dependency Budget & Supply Chain (Strict runtime cap <= 8, no heavy sprawl)
3. Agent Plugin & Skill Hygiene (Zero enterprise cloud skills)
4. Architectural Simplicity & Cognitive Budget (KISS/YAGNI, max file complexity)
5. Toolchain Consolidation (Single tool for linting, testing, dependencies)
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class SoloMaintainerAudit:
    def __init__(self, root: Path, strict: bool = False):
        self.root = root
        self.strict = strict
        self.results: dict[str, list[dict[str, Any]]] = {
            "Language Monoculture": [],
            "Dependency & Supply Chain Budget": [],
            "Agent Plugin & Skill Hygiene": [],
            "Architectural Simplicity & Cognitive Budget": [],
            "Toolchain Consolidation": [],
        }
        self.all_passed = True
        self.warnings_count = 0
        self.failures_count = 0

    def record(
        self,
        category: str,
        name: str,
        passed: bool,
        details: str,
        remediation: str = "",
        is_warning: bool = False,
    ) -> None:
        if not passed:
            if is_warning and not self.strict:
                self.warnings_count += 1
            else:
                self.failures_count += 1
                self.all_passed = False

        self.results[category].append(
            {
                "name": name,
                "passed": passed,
                "is_warning": is_warning and not self.strict,
                "details": details,
                "remediation": remediation,
            }
        )

    # -------------------------------------------------------------------------
    # 1. LANGUAGE MONOCULTURE CHECKS
    # -------------------------------------------------------------------------
    def audit_language_monoculture(self) -> None:
        """Enforces 100% Python monoculture with zero unauthorized sprawl."""
        category = "Language Monoculture"

        forbidden_extensions = {
            ".js": "JavaScript runtime (Node.js/npm) sprawl",
            ".jsx": "React/Frontend framework sprawl",
            ".ts": "TypeScript runtime sprawl",
            ".tsx": "React/TypeScript frontend sprawl",
            ".rs": "Rust compilation toolchain overhead",
            ".go": "Go runtime and compilation overhead",
            ".c": "Native C compilation overhead",
            ".cpp": "C++ compilation toolchain overhead",
            ".java": "JVM runtime overhead",
            ".kt": "Kotlin/JVM runtime overhead",
            ".rb": "Ruby runtime sprawl",
            ".php": "PHP runtime sprawl",
            ".cs": ".NET runtime sprawl",
        }

        forbidden_configs = {
            "package.json": "Node.js npm package manager",
            "package-lock.json": "npm lockfile",
            "yarn.lock": "Yarn package manager",
            "pnpm-lock.yaml": "pnpm package manager",
            "Cargo.toml": "Rust Cargo package manager",
            "go.mod": "Go module manifest",
            "Gemfile": "Ruby Bundler manifest",
            "composer.json": "PHP Composer manifest",
        }

        ignored_dirs = {
            ".git",
            ".venv",
            "venv",
            ".pytest_cache",
            ".ruff_cache",
            ".mypy_cache",
            "__pycache__",
            ".hypothesis",
            ".devcontainer",
            "node_modules",
            "dist",
            "build",
        }

        found_foreign_files: list[tuple[str, str]] = []
        found_foreign_configs: list[tuple[str, str]] = []

        for root_dir, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            rel_dir = Path(root_dir).relative_to(self.root)

            # Skip docs and assets from strict JS/HTML asset checks
            if str(rel_dir).startswith("docs") or str(rel_dir).startswith("assets"):
                continue

            for file in files:
                file_path = Path(root_dir) / file
                rel_path = file_path.relative_to(self.root)

                if file in forbidden_configs:
                    found_foreign_configs.append(
                        (str(rel_path), forbidden_configs[file])
                    )

                ext = file_path.suffix.lower()
                if ext in forbidden_extensions:
                    found_foreign_files.append(
                        (str(rel_path), forbidden_extensions[ext])
                    )

        if found_foreign_configs:
            details = "Forbidden foreign package managers detected:\n" + "\n".join(
                f"  - `{p}` ({r})" for p, r in found_foreign_configs
            )
            self.record(
                category,
                "Foreign Package Managers",
                False,
                details,
                "Remove secondary language manifests. Maintain pure Python.",
            )
        else:
            self.record(
                category,
                "Foreign Package Managers",
                True,
                "Zero secondary package managers (npm, cargo, go) detected.",
            )

        if found_foreign_files:
            details = "Unauthorized non-Python source files detected:\n" + "\n".join(
                f"  - `{p}` ({r})" for p, r in found_foreign_files
            )
            self.record(
                category,
                "Pure Python Source Monoculture",
                False,
                details,
                "Consolidate logic into standard library, FastAPI, or Pydantic.",
            )
        else:
            self.record(
                category,
                "Pure Python Source Monoculture",
                True,
                "Codebase adheres to 100% Python monoculture (no polyglot sprawl).",
            )

    # -------------------------------------------------------------------------
    # 2. DEPENDENCY & SUPPLY CHAIN BUDGET
    # -------------------------------------------------------------------------
    def audit_dependencies(self) -> None:
        """Enforces a strict dependency budget to prevent maintenance rot."""
        category = "Dependency & Supply Chain Budget"
        pyproject_path = self.root / "pyproject.toml"

        if not pyproject_path.exists():
            self.record(
                category,
                "pyproject.toml Manifest",
                False,
                "Missing pyproject.toml",
                "Ensure pyproject.toml is configured at the workspace root.",
            )
            return

        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
        except Exception as exc:
            self.record(
                category,
                "pyproject.toml Parsing",
                False,
                f"Error parsing pyproject.toml: {exc}",
                "Fix syntax errors in pyproject.toml.",
            )
            return

        dependencies = data.get("project", {}).get("dependencies", [])
        dep_count = len(dependencies)
        max_budget = 8

        forbidden_heavy_packages = {
            "tensorflow": "High binary size and fragile native C++ bindings",
            "torch": "Massive wheel footprint (>2GB) and breaking API churn",
            "celery": "Requires external Redis/RabbitMQ message brokers",
            "redis": "Requires running an external stateful daemon",
            "kafka": "Requires distributed JVM message bus",
            "pyspark": "Requires Apache Spark JVM and Hadoop runtime",
            "django": "Monolithic framework overhead; FastAPI suffices",
            "flask": "Redundant web framework alongside FastAPI",
            "airflow": "Enterprise scheduler requiring dedicated database & daemon",
        }

        detected_heavy: list[str] = []
        parsed_dep_names: list[str] = []

        for dep in dependencies:
            match = re.match(r"^([A-Za-z0-9_\-]+)", dep.strip())
            if match:
                pkg_name = match.group(1).lower()
                parsed_dep_names.append(pkg_name)
                if pkg_name in forbidden_heavy_packages:
                    detected_heavy.append(
                        f"{pkg_name} ({forbidden_heavy_packages[pkg_name]})"
                    )

        if dep_count <= max_budget:
            self.record(
                category,
                "Runtime Dependency Budget",
                True,
                f"Active runtime dependencies: {dep_count}/{max_budget} "
                "(within budget).",
            )
        else:
            diff = dep_count - max_budget
            self.record(
                category,
                "Runtime Dependency Budget",
                False,
                f"Active runtime dependencies: {dep_count}/{max_budget} "
                f"(exceeds budget by {diff}).",
                f"Audit pyproject.toml. Limit direct packages to <= {max_budget}.",
            )

        if detected_heavy:
            self.record(
                category,
                "Heavyweight / Daemon Proscription",
                False,
                "Detected heavyweight or external-daemon dependencies:\n"
                + "\n".join(f"  - {d}" for d in detected_heavy),
                "Remove heavy dependencies and replace with stdlib or Supabase.",
            )
        else:
            self.record(
                category,
                "Heavyweight / Daemon Proscription",
                True,
                "Zero heavyweight (PyTorch/Spark) or broker (Celery/Kafka) deps.",
            )

        uv_lock = self.root / "uv.lock"
        if uv_lock.exists() and uv_lock.stat().st_size > 0:
            size_kb = uv_lock.stat().st_size // 1024
            self.record(
                category,
                "Deterministic uv.lock File",
                True,
                f"uv.lock is present and non-empty ({size_kb} KB).",
            )
        else:
            self.record(
                category,
                "Deterministic uv.lock File",
                False,
                "uv.lock is missing or empty.",
                "Run `uv lock` to generate a deterministic lockfile.",
            )

    # -------------------------------------------------------------------------
    # 3. AGENT PLUGIN & SKILL HYGIENE
    # -------------------------------------------------------------------------
    def audit_agent_skills(self) -> None:
        """Audits .agents/skills to prevent enterprise cloud skill pollution."""
        category = "Agent Plugin & Skill Hygiene"
        skills_dir = self.root / ".agents" / "skills"

        if not skills_dir.exists():
            self.record(
                category,
                "Workspace Agent Skills Directory",
                True,
                "No local `.agents/skills` override directory present.",
            )
            return

        cloud_enterprise_skills = {
            "bigquery-data-transfer-service",
            "building-data-apps",
            "data-autocleaning",
            "dataform-bigquery",
            "dbt-bigquery",
            "developing-with-bigquery",
            "discovering-gcp-data-assets",
            "federate-lakehouse-catalog",
            "gcloud-auth-verification",
            "gcp-composer-troubleshooting",
            "gcp-data-pipelines",
            "gcp-dataflow",
            "gcp-pipeline-orchestration",
            "gcp-pipeline-resource-provisioning",
            "gcp-spark",
            "notebook-guidance",
            "bigquery-ai-ml",
            "bigquery-sql",
            "bigtable-basics",
        }

        installed = [
            d.name
            for d in skills_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        detected_cloud = [s for s in installed if s in cloud_enterprise_skills]
        total_skills = len(installed)

        if detected_cloud:
            details = (
                f"Detected {len(detected_cloud)} out-of-scope enterprise GCP "
                f"skills in `.agents/skills/` (Total: {total_skills}):\n"
                + "\n".join(f"  - {s}" for s in detected_cloud[:6])
            )
            if len(detected_cloud) > 6:
                details += f"\n  - ... and {len(detected_cloud) - 6} more."

            remediation = (
                "Prune out-of-scope cloud skills from `.agents/skills/`. Keep only "
                "repository-relevant skills (code-quality, companion, handoff)."
            )

            self.record(
                category,
                "Enterprise Cloud Skill Pollution",
                False,
                details,
                remediation,
                is_warning=not self.strict,
            )
        else:
            self.record(
                category,
                "Enterprise Cloud Skill Pollution",
                True,
                f"Clean workspace skills ({total_skills} domain skills, zero cloud).",
            )

        essential = ["code-quality", "code-companion", "agent-handoff"]
        missing = [s for s in essential if s not in installed]
        if missing:
            self.record(
                category,
                "Essential EthoPipe Skills",
                False,
                f"Missing recommended agent skills: {missing}",
                "Ensure core workflow skills are present in `.agents/skills/`.",
            )
        else:
            self.record(
                category,
                "Essential EthoPipe Skills",
                True,
                "Core agent skills (code-quality, companion, handoff) present.",
            )

    # -------------------------------------------------------------------------
    # 4. ARCHITECTURAL SIMPLICITY & COGNITIVE BUDGET
    # -------------------------------------------------------------------------
    def audit_architecture_simplicity(self) -> None:
        """Enforces KISS/YAGNI principles: no monolith files, no k8s sprawl."""
        category = "Architectural Simplicity & Cognitive Budget"

        forbidden_infra = [
            "k8s",
            "kubernetes",
            "helm",
            "terraform",
            "nomad",
            "ansible",
        ]
        found_infra: list[str] = []
        for item in self.root.iterdir():
            if item.name.lower() in forbidden_infra:
                found_infra.append(item.name)

        if found_infra:
            self.record(
                category,
                "Infrastructure Overhead",
                False,
                f"Found enterprise infrastructure configurations: {found_infra}",
                "Keep deployment minimal (Docker Compose / single container).",
            )
        else:
            self.record(
                category,
                "Infrastructure Overhead",
                True,
                "Zero enterprise Kubernetes/Helm/Terraform infrastructure bloat.",
            )

        src_dir = self.root / "src"
        max_lines_per_file = 600
        bloated_files: list[tuple[str, int]] = []

        if src_dir.exists():
            for root_dir, _, files in os.walk(src_dir):
                for f in files:
                    if f.endswith(".py"):
                        p = Path(root_dir) / f
                        try:
                            lines = len(
                                p.read_text(
                                    encoding="utf-8", errors="replace"
                                ).splitlines()
                            )
                            if lines > max_lines_per_file:
                                rel = p.relative_to(self.root)
                                bloated_files.append((str(rel), lines))
                        except Exception:
                            pass

        if bloated_files:
            details = f"Files exceeding {max_lines_per_file} lines:\n"
            for rel, count in bloated_files:
                details += f"  - `{rel}`: {count} lines\n"
            self.record(
                category,
                "Single-File Cognitive Limit (< 600 lines)",
                False,
                details.strip(),
                "Refactor oversized files into focused, modular components.",
                is_warning=True,
            )
        else:
            self.record(
                category,
                "Single-File Cognitive Limit (< 600 lines)",
                True,
                f"All files in `src/` are bounded under {max_lines_per_file} lines.",
            )

    # -------------------------------------------------------------------------
    # 5. TOOLCHAIN CONSOLIDATION
    # -------------------------------------------------------------------------
    def audit_toolchain(self) -> None:
        """Enforces a single-tool-per-job rule to minimize developer friction."""
        category = "Toolchain Consolidation"

        conflicting_tools = [
            ".flake8",
            ".pylintrc",
            "setup.cfg",
            ".isort.cfg",
            ".black",
        ]
        found_conflicts = [f for f in conflicting_tools if (self.root / f).exists()]

        if found_conflicts:
            self.record(
                category,
                "Linter & Formatter Consolidation",
                False,
                f"Legacy linter configs found: {found_conflicts}",
                "Remove legacy configs and standardize 100% on `ruff`.",
            )
        else:
            self.record(
                category,
                "Linter & Formatter Consolidation",
                True,
                "Toolchain cleanly consolidated on Ruff (replaces black, isort).",
            )

        qa_runner = self.root / "scripts" / "run_qa.ps1"
        if qa_runner.exists():
            self.record(
                category,
                "Single-Command QA Pipeline",
                True,
                "Runner `scripts/run_qa.ps1` configured for zero-friction audit.",
            )
        else:
            self.record(
                category,
                "Single-Command QA Pipeline",
                False,
                "Missing `scripts/run_qa.ps1`.",
                "Provide a unified one-line QA script for the solo maintainer.",
            )

    # -------------------------------------------------------------------------
    # EXECUTION & REPORT GENERATION
    # -------------------------------------------------------------------------
    def run_all(self) -> bool:
        sep = "═" * 64
        print(f"\n{BOLD}{CYAN}{sep}{RESET}")
        title = "EthoPipe Solo Maintainer Guardrails & Anti-Bloat Audit"
        print(f"{BOLD}{CYAN}   {title}{RESET}")
        print(f"{BOLD}{CYAN}{sep}{RESET}\n")

        self.audit_language_monoculture()
        self.audit_dependencies()
        self.audit_agent_skills()
        self.audit_architecture_simplicity()
        self.audit_toolchain()

        self._print_terminal_summary()
        self._write_markdown_report()

        return self.all_passed

    def _print_terminal_summary(self) -> None:
        for category, checks in self.results.items():
            print(f"{BOLD}[+] {category}{RESET}")
            for check in checks:
                if check["passed"]:
                    print(f"  {GREEN}[✓] PASS:{RESET} {check['name']}")
                elif check["is_warning"]:
                    print(f"  {YELLOW}[!] WARN:{RESET} {check['name']}")
                    for line in check["details"].splitlines():
                        print(f"      {line}")
                else:
                    print(f"  {RED}[✗] FAIL:{RESET} {check['name']}")
                    for line in check["details"].splitlines():
                        print(f"      {line}")
                    if check["remediation"]:
                        print(f"      {CYAN}Remediation:{RESET} {check['remediation']}")
            print()

        sep = "═" * 64
        print(f"{BOLD}{sep}{RESET}")
        if self.all_passed:
            if self.warnings_count > 0:
                print(
                    f"{GREEN}{BOLD}🎉 PASSED with {self.warnings_count} warning(s): "
                    f"Codebase complies with Solo Maintainer Guardrails!{RESET}\n"
                )
            else:
                print(
                    f"{GREEN}{BOLD}🎉 PERFECT: Zero bloat detected. "
                    f"Sustainable for solo maintainer!{RESET}\n"
                )
        else:
            print(
                f"{RED}{BOLD}❌ AUDIT FAILED: {self.failures_count} violation(s) "
                f"threatening solo sustainability.{RESET}\n"
            )

    def _write_markdown_report(self) -> None:
        report_path = self.root / "docs" / "SOLO_MAINTAINER_AUDIT.md"
        now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%SZ")

        badge = (
            "![Status](https://img.shields.io/badge/Solo_Maintainer_Audit-PASSING-brightgreen)"
            if self.all_passed
            else "![Status](https://img.shields.io/badge/Solo_Maintainer_Audit-FAILED-red)"
        )

        md = [
            "# Solo Maintainer Guardrails & Anti-Bloat Audit Report",
            "",
            f"**Generated:** `{now}`  ",
            f"**Audit Mode:** `{'Strict' if self.strict else 'Standard'}`  ",
            f"**Verdict:** {badge}",
            "",
            "## Executive Summary",
            "",
            "This automated scorecard enforces the **EthoPipe Solo Maintainer "
            "Charter**: protecting the repository from dependency creep, polyglot "
            "sprawl, out-of-scope enterprise cloud plugins, and cognitive debt.",
            "",
            "| Pillar | Status | Passed | Issues |",
            "| :--- | :---: | :---: | :---: |",
        ]

        for cat, checks in self.results.items():
            passed = sum(1 for c in checks if c["passed"])
            failed = sum(1 for c in checks if not c["passed"])
            if failed == 0:
                cat_status = "✅ PASS"
            elif any(c["is_warning"] for c in checks if not c["passed"]):
                cat_status = "⚠️ WARN"
            else:
                cat_status = "❌ FAIL"
            md.append(f"| {cat} | {cat_status} | {passed}/{len(checks)} | {failed} |")

        md.extend([
            "",
            "---",
            "",
            "## Detailed Check Breakdown",
            "",
        ])

        for cat, checks in self.results.items():
            md.append(f"### {cat}")
            md.append("")
            for c in checks:
                icon = "✅" if c["passed"] else ("⚠️" if c["is_warning"] else "❌")
                md.append(f"#### {icon} {c['name']}")
                md.append("")
                md.append(f"**Details:**\n```text\n{c['details']}\n```")
                if not c["passed"] and c["remediation"]:
                    md.append(f"**Action Required:** {c['remediation']}")
                md.append("")

        md.extend([
            "---",
            "",
            "## The 5 Invariants of the Solo Maintainer Charter",
            "",
            "1. **Language Monoculture**: 100% Python (>= 3.11). Zero secondary compiled or JavaScript runtimes.",
            "2. **Strict Dependency Budget**: Maximum 8 runtime packages in `pyproject.toml`. No heavy AI or broker daemons.",
            "3. **Skill & Plugin Cleanliness**: Zero out-of-scope enterprise cloud skills (GCP, BigQuery, Airflow, Spark).",
            "4. **Architectural Simplicity**: Pure modular Python. Files strictly bounded under 600 lines. Single Docker container.",
            "5. **Unified Toolchain**: Exclusively `uv`, `ruff`, `mypy`, `pytest` with a single-command QA script (`run_qa.ps1`).",
        ])

        report_path.write_text("\n".join(md), encoding="utf-8")
        print(f"{CYAN}[✓] Audit report written to: {report_path}{RESET}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify repository compliance with Solo Maintainer Guardrails."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat all warnings (e.g. cloud skill pollution) as blocking failures.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    auditor = SoloMaintainerAudit(root=root, strict=args.strict)
    success = auditor.run_all()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
