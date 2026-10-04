## Summary & Objective
<!-- Briefly state the purpose, context, and motivation for this change. -->

### Related Issues
<!-- Link related issues: e.g. Fixes #123, Closes #456 -->
- Closes #

## Track Classification
<!-- Select the primary track governing this PR -->
- [ ] ⚡ `track:bolt` (Performance, caching, vectorization)
- [ ] 🛡️ `track:sentinel` (Security, sanitization, boundary defense)
- [ ] 📦 `track:feature` (Schema, Darwin Core mapping, parser)
- [ ] 🔧 `track:refactor` (Simplification, modularization)
- [ ] 🛠️ `track:maintainer` (Governance, scripts, workflows, CI/CD)

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] ✨ New feature (non-breaking change adding functionality)
- [ ] ⚡ Performance improvement
- [ ] 🛡️ Security hardening
- [ ] ♻️ Refactoring / Code cleanup
- [ ] 📝 Documentation update
- [ ] 🤖 Agent & CI/CD workflow automation

## Verification & Testing
<!-- Describe the tests and verification steps performed. Provide command outputs or proof of correctness. -->
```bash
# Example local verification:
uv run pytest tests/ --cov=src
uv run python scripts/audit_maintainer_guardrails.py
uv run python scripts/verify_open_source_standards.py
```

## Mandatory Quality Gates (All Must Be Verified)
- [ ] **Solo Maintainer Charter**: 100% pure Python (>= 3.11), <= 8 direct dependencies, zero external broker daemons.
- [ ] **Biological & Schema Invariants**: Canine heart rate clamped to [30, 250] BPM, Darwin Core `MeasurementOrFact` standard, strict Pydantic v2 validation.
- [ ] **Test Coverage**: Unit tests or Hypothesis property-based boundary tests added/updated; repository coverage remains >= 85%.
- [ ] **Cognitive Complexity**: No Python file in `src/` exceeds 600 lines.
- [ ] **Local QA**: `.\scripts\run_qa.ps1` (or local equivalent) executed with all steps passing.
- [ ] **Journal & Documentation**:
  - [ ] Recorded in `.jules/bolt.md` (if performance/vectorization)
  - [ ] Recorded in `.jules/sentinel.md` (if security/hardening)
  - [ ] Recorded in `CHANGELOG.md` (if user-facing feature/fix)
  - [ ] Recorded in `JOURNEY.md` (if session milestone/architectural decision)
