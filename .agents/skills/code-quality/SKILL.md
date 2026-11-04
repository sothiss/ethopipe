---
name: code-quality
description: Enforces institutional-grade code quality, static type safety, 85%+ test coverage, and open-source standards compliance (JOSS, FAIR principles, OSI licensing, Citation CFF).
---

# Code Quality & Open Source Standards Skill

Use this skill to audit repository compliance, run quality gates, and verify open-science benchmarks before committing code or submitting pull requests.

## Trigger Commands

### Full Open Source Standards Audit
```bash
python scripts/verify_open_source_standards.py
```
Outputs compliance scorecard to `docs/OPEN_SOURCE_COMPLIANCE.md`.

### Comprehensive 8-Step QA Runner
```powershell
.\scripts\run_qa.ps1
```

## The 5 Verification Pillars
1. **Static Quality**: `ruff format --check src tests`, `ruff check src tests`, `mypy src`.
2. **Test Baseline**: Full `pytest` suite passing, `>= 85%` line coverage, Hypothesis boundary fuzzing (`tests/test_adversarial_boundaries.py`).
3. **Biological Invariants**: Pydantic v2 strict mode (`ConfigDict(strict=True)`), canine HR `[30, 250]` BPM, Darwin Core `MeasurementOrFact`, linguistic neutrality.
4. **Governance**: `LICENSE` (MIT), `CITATION.cff`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/ai-usage.md`.
5. **Supply Chain**: `uv lock --check`, `uv audit` with zero CVEs.

## Quick Remediation Reference

| Failure Mode | Root Cause | Remediation Command |
| :--- | :--- | :--- |
| **Formatting Failure** | Unformatted Python lines | `ruff format src tests scripts` |
| **Lint Violations** | Dead code, deprecated syntax | `ruff check --fix src tests scripts` |
| **Mypy Type Error** | Untyped kwargs or missing annotations | Use `Model.model_validate(dict)` or add explicit type hints |
| **Coverage < 85%** | Untested execution paths | Add unit test cases in `tests/` |
| **Lockfile Drift** | `pyproject.toml` changed without lock | `uv lock` |
