# EthoPipe Code Quality & Open Source Standards

## 1. Overview & Vision

EthoPipe is developed under open-science reproducibility standards to eliminate the replication crisis and data fragmentation bottleneck in applied canine ethology. To ensure that the software and its data models are institutionally viable for peer review, multi-center epidemiological research, and long-term citation, the project adheres to:

1. **JOSS (Journal of Open Source Software) Benchmarks**: Verifiable statement of need, clear installation and quickstart walkthroughs, comprehensive documentation, community guidelines, and automated regression testing.
2. **FAIR Data Principles**: Making observational telemetry **Findable, Accessible, Interoperable, and Reusable** via native Darwin Core (DwC) metadata standards.
3. **OSI-Approved Open Source Governance**: Permissive licensing (MIT), formal citation specifications (`CITATION.cff`), contributor covenants, and vulnerability disclosure policies.

---

## 2. The 5 Standards Pillars

```
┌────────────────────────────────────────────────────────────────────────┐
│                   EthoPipe Open Science Standards                       │
├─────────────────┬─────────────────┬──────────────────┬─────────────────┤
│ Static & Type   │ Testing & Fuzz  │ Domain & DwC     │ Governance &    │
│ Integrity       │ Baseline        │ Invariants       │ Community       │
│ • Ruff Format   │ • Pytest (92%)  │ • Pydantic v2    │ • MIT License   │
│ • Ruff Lint     │ • Hypothesis    │ • DwC Mapping    │ • CITATION.cff  │
│ • Mypy (Strict) │ • Adversarial   │ • HR Clamping    │ • Code Conduct  │
│ • Pre-commit    │ • Coverage >=85%│ • De-biasing     │ • JOSS Readme   │
└─────────────────┴─────────────────┴──────────────────┴─────────────────┘
```

### Pillar 1: Code Quality & Static Integrity
- **Formatting**: Enforced via `ruff format --check src tests` with an 88-character line length limit.
- **Linting**: Enforced via `ruff check src tests` with rulesets `E`, `F`, `I` (isort), `UP` (pyupgrade), `B` (bugbear), `SIM` (simplify), and `RUF`.
- **Type Safety**: Enforced via `mypy src` with `pydantic.mypy` plugin and `pandas-stubs` for type checking.

### Pillar 2: Testing Baseline & Adversarial Boundaries
- **Unit & Functional Suite**: 22 passing tests in `tests/` covering API endpoints, data models, and edge cases.
- **Coverage Requirement**: Total line coverage must remain above **85%** (currently verified at **92%**).
- **Hypothesis Property Testing**: Fuzzes non-standard, malformed, and adversarial vital inputs (`tests/test_adversarial_boundaries.py`) to prove model resilience against corrupted data entry.

### Pillar 3: Domain Invariants & Open Science
- **Pydantic v2 Strict Mode**: All models enforce `model_config = ConfigDict(strict=True)` to prevent silent type coercion.
- **Veterinary Physiological Bounds**: Canine heart rates are clamped strictly between `30` and `250` BPM (Toy: `80–200` BPM; Giant: `40–110` BPM).
- **Darwin Core (DwC) Standardization**: Observations map to `MeasurementOrFact` (`dwc:individualID`, `dwc:eventDate`, `dwc:measurementType`, `dwc:measurementValue`, `dwc:basisOfRecord`).
- **Linguistic Neutrality**: Subjective anthropomorphic terms (`stubborn`, `angry`, `spiteful`) are actively scrubbed from handler notes.
- **AI Governance**: Disclosed in `docs/ai-usage.md` with zero-temperature parsing constraints.

### Pillar 4: Open Source Governance & Community
- **License**: OSI-approved MIT License in [`LICENSE`](file:///H:/Projects/ethopipe/LICENSE).
- **Software Citation**: Machine-readable [`CITATION.cff`](file:///H:/Projects/ethopipe/CITATION.cff) following CFF v1.2.0 with author ORCID deposit.
- **Code of Conduct**: Contributor Covenant v2.1 in [`CODE_OF_CONDUCT.md`](file:///H:/Projects/ethopipe/CODE_OF_CONDUCT.md).
- **Contribution Guidelines**: Clear pull request and development instructions in [`CONTRIBUTING.md`](file:///H:/Projects/ethopipe/CONTRIBUTING.md).
- **Security Policy**: Responsible disclosure process in [`SECURITY.md`](file:///H:/Projects/ethopipe/SECURITY.md).

### Pillar 5: Supply Chain & Dependency Health
- **Deterministic Lockfile**: `uv.lock` must remain synchronized with `pyproject.toml` (`uv lock --check`).
- **Security Audits**: Continuous scanning via `uv audit` against the PyPA vulnerability database to ensure zero CVE exposure.

---

## 3. Automated Verification Tooling

### 1. Programmatic Standards Audit
Run the automated standards engine:

```bash
python scripts/verify_open_source_standards.py
```

This generates the real-time compliance scorecard in [`docs/OPEN_SOURCE_COMPLIANCE.md`](file:///H:/Projects/ethopipe/docs/OPEN_SOURCE_COMPLIANCE.md).

### 2. Full 7-Step QA Runner
Run the comprehensive test and enforcement suite:

```powershell
.\scripts\run_qa.ps1
```

Executes:
1. Environment audit (`uv pip list`, `uv audit`)
2. Format & style gates (`ruff format`, `ruff check`)
3. Type safety checks (`mypy`)
4. Full test suite with coverage (`pytest --cov=src`)
5. Adversarial boundary audit (`pytest tests/test_adversarial_boundaries.py`)
6. Git hook enforcement (`pre-commit run --all-files`)
7. Open Source & Open Science Standards Audit (`scripts/verify_open_source_standards.py`)
