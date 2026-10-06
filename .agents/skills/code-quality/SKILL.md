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

### Comprehensive 7-Step QA Runner
```powershell
.\scripts\run_qa.ps1
```

## The 5 Verification Pillars
1. **Static Quality**: `ruff format`, `ruff check`, `mypy`.
2. **Test Baseline**: 22+ tests passing, >=85% line coverage, Hypothesis boundary fuzzing.
3. **Biological Invariants**: Pydantic v2 strict mode, canine HR 30-250 BPM, Darwin Core `MeasurementOrFact`.
4. **Governance**: `LICENSE` (MIT), `CITATION.cff`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`.
5. **Supply Chain**: `uv lock --check`, `uv audit` with zero CVEs.
