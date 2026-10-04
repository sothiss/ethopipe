================================================================================
CODE COMPANION (JULES) TASK BRIEF (PASTE INTO GITHUB ISSUE / COMPANION PROMPT)
================================================================================

# Task Brief: 🛡️ Sentinel: Validate maximum length boundary on handler_notes

**Target Companion:** Google Labs Jules (`@google-labs-jules[bot]`) / Companion
**Task Track:** `SENTINEL`
**Target Branch:** `main`
**Recommended PR Title:** `🛡️ Sentinel: Validate maximum length boundary on handler_notes`

---

## 1. Primary Objective
Validate maximum length boundary on handler_notes

---

## 2. Strict Modification Boundaries (Scope Control)
You are STRICTLY constrained to modify ONLY the following files:
- `src/pipeline/models.py`
- `tests/test_models.py`

Do NOT modify project configuration files (`pyproject.toml`,
`.pre-commit-config.yaml`, CI workflows) unless specifically authorized.

---

## 3. Required Implementation Steps
1. Inspect working tree status
2. Continue with assigned feature/bugfix objective
3. Run tests via pytest

---

## 4. Inviolable Repository Invariants (Do Not Violate)
1. **Pydantic v2 Strict Mode**: All models must have
   `model_config = ConfigDict(strict=True)`.
2. **Canine Heart Rate Bounds**: Clamped strictly between 30 and 250 BPM
   (Toy: 80-200 BPM, Giant: 40-110 BPM).
3. **Darwin Core (DwC)**: Behavioral syllables map to `MeasurementOrFact`
   (`dwc:individualID`, `dwc:eventDate`, `dwc:measurementType`,
   `dwc:measurementValue`, `dwc:basisOfRecord`).
4. **Linguistic De-biasing**: Discard subjective labels ('stubborn', 'spiteful')
   in favor of objective motor postures.
5. **Zero Test Regressions**: Current baseline has 22 passing tests.

---

## 5. Mandatory Verification Commands
Before submitting your pull request, you MUST execute and pass:
```bash
pytest tests/ --tb=short -q
ruff format --check src tests
ruff check src tests
```

### Mandatory Learning Journal Update (.jules/sentinel.md)
Upon completing this security hardening, you MUST append a learning entry to
`.jules/sentinel.md`:
```markdown
## YYYY-MM-DD - <Topic>
**Learning:** <Vulnerability, input length boundary, or DoS vector resolved>
**Action:** <Pydantic validation or sanitization rule enforced>
```


---

## 6. Known Context & Warnings
None. All baselines verified and passing.

*Reference Snapshot: `docs/LLM_SNAPSHOT.md` | Status: `docs/AGENT_HANDOFF.md`*
================================================================================
