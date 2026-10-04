# [IDEA-001] Darwin Core observation batch deduplication

**Track:** `bolt` | **Created:** `2026-10-04` | **Status:** `in-triage`
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
- [ ] **All 8 Steps Pass**: Run `.\scripts\run_qa.ps1` with 0 failures.
- [ ] **Journal Updated**:
  - If `bolt`: Append learning entry to `.jules/bolt.md`.
  - If `sentinel`: Append defensive entry to `.jules/sentinel.md`.
  - If `feat` / `refactor`: Update `CHANGELOG.md`.

---

## 📝 Implementation Notes & Scratchpad
*Log commands, profiling data, or code snippets here during development.*
