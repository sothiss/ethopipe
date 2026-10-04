## Summary & Objective
<!-- Briefly state the exact micro-objective of this pull request -->

## Track Classification
- [ ] ⚡ `track:bolt` (Performance, caching, vectorization)
- [ ] 🛡️ `track:sentinel` (Security, sanitization, boundary defense)
- [ ] 📦 `track:feature` (Schema, Darwin Core mapping, parser)
- [ ] 🔧 `track:refactor` (Simplification, modularization)
- [ ] 🛠️ `track:maintainer` (Governance, scripts, workflows)

## Anti-Skipping Quality Gates (Must Check All Before Merging)
- [ ] **1. Solo Maintainer Charter**: 100% pure Python, <= 8 direct dependencies, zero broker daemons.
- [ ] **2. Biological & Technical Invariants**: Canine HR clamped to [30, 250] BPM, DwC MeasurementOrFact, strict Pydantic v2.
- [ ] **3. Tests First**: Unit test or Hypothesis boundary property test added or updated.
- [ ] **4. Complexity Limit**: Modified files in `src/` remain strictly under 600 lines.
- [ ] **5. Full QA Execution**: `.\scripts\run_qa.ps1` executed locally with all 8 steps passing.
- [ ] **6. Journal / Changelog Closure**:
  - [ ] Appended to `.jules/bolt.md` (if Bolt)
  - [ ] Appended to `.jules/sentinel.md` (if Sentinel)
  - [ ] Appended to `CHANGELOG.md` (if Feature or Refactor)
