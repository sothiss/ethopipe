# EthoPipe Idea & Task Board

**Last Synchronized:** `2026-10-04 18:06:02Z`
**Pipeline Status:** Active Step-Gated Anti-Skipping System

## 📋 Active Tasks & Ideas

| ID | Track | Title | Current Gate | Progress | File |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **IDEA-001** | `bolt` | Darwin Core observation batch deduplication | `Gate 1: Triage & Solo Maintainer Veto` | 0/15 (0%) | [IDEA-001](docs/ideas/IDEA-001_darwin-core-observation-batch-deduplication.md) |

---

## 🔒 The 5-Gate Sequence

1. **Gate 1: Triage & Solo Maintainer Veto** — Language monoculture, dependency budget, and YAGNI.
2. **Gate 2: Boundary Specification** — Target files, Darwin Core mapping, and physiological limits.
3. **Gate 3: Adversarial Test First** — Writing the test/Hypothesis case *before* production code.
4. **Gate 4: Minimal Implementation (KISS)** — Clean, strict Pydantic v2 under 600 lines.
5. **Gate 5: QA & Journal Verification** — All 8 steps of `.\scripts\run_qa.ps1` + journal logging.

### CLI Commands
```powershell
# Create a new idea
.\scripts\idea.ps1 -New "My Idea" -Track bolt

# Audit that no gates were skipped
python scripts/manage_ideas.py audit
```
