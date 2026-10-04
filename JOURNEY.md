# Research Software Engineering (RSE) Log: EthoPipe Journey
**Project Architecture:** EthoPipe (The Transparency Project 1.0)
**Principal Investigator:** Alice Severi Gonçalves (ORCID: 0009-0003-0048-8982)
**Methodological Paradigm:** Open Science, Computational Canine Ethology, and Deterministic Data Pipelines

---

## 📊 System Environment Parameters Matrix
This matrix tracks the invariant technical boundaries of the execution layer to eliminate "it works on my machine" syndrome and prevent dependency drift.

| Parameter | Baseline Configuration | Target Specification | Status |
| :--- | :--- | :--- | :--- |
| **Runtime Language** | Python 3.11 Virtual Env (`.venv`) | Isolated Docker Environment | Stable |
| **Core Validation Engine** | Pydantic v2 BaseModel Constraints | Strict Type Enforcement Gatekeeper | Passing (43 Tests) |
| **Semantic Parser** | Google AI Studio Sandbox | Serverless Cloud Ingestion API | Prototyping |
| **Metadata Informatics** | Custom Data Dictionary | International Darwin Core (DwC) Mapping | Mapped |
| **Governance Stack** | Local Version Control | GitHub Actions CI/CD + Protected `main` | Structured |

---

## 📓 Chronological Evolution & Architectural Logs

### Entry 001: The Systemic Clean Slate & History Reset
* **Date & Model:** 2025-11-15 | Gemini 1.5 Pro | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Environmental Anomalies & Git History Friction
* **The Technical Challenge:** The local development environment was suffering from compounding configuration debt. Bloated IDE extensions (Azure/Kubernetes proxies) were polluting execution paths, while raw Google Cloud Application Default Credentials (ADC) endpoints were misaligned. The local version control history had devolved into volatile tracking cycles.
* **The Architectural Pivot:** Performed an explicit "intellectual garbage collection."
  1. Ruthlessly pruned the IDE extension panels to maximize processing bandwidth.
  2. Executed an operational Git reset to eliminate tracking clutter and establish a sterile repository baseline.
  3. Re-authenticated cloud credentials globally via `gcloud auth application-default login` outside the immediate codebase paths.
* **Quantitative Milestone:** A pristine, standardized root repository structure (`src/`, `tests/`, `docs/`) deployed safely to a single tracking line on `main` at `github.com/sothiss/ethopipe`.

### Entry 002: Hardcoding Biological Realities into the Pydantic Matrix
* **Date & Model:** 2025-12-02 | Gemini 1.5 Pro | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Semantic Ingestion Bias vs. Deterministic Gatekeeping
* **The Technical Challenge:** Unstructured field narratives and handler logs contain high frequencies of anthropomorphic, subjective terms (e.g., "Max was being stubborn and protective"). Furthermore, manual data entries introduce extreme physiological anomalies that can corrupt downstream quantitative analytical engines.
* **The Architectural Pivot:** Translated paper-based canine behavior literature (Hsu & Serpell's C-BARQ parameters, Bekoff, Handelman, and 2024 peer-reviewed ethograms) directly into immutable Python code blocks. Hardcoded biological guardrails into Pydantic models:
  * Restricting viable heart rates strictly between $30$ and $250$ BPM (flagging anomalous values like 380 or 400 BPM as immediate `ValidationError` exceptions).
  * Coercing behavioral observations strictly into validated Enums (`play_bow`, `licking_of_lips`, `looking_away`, `posture_freeze`).
* **Quantitative Milestone:** Successfully built and verified a 43-test passing validation validation loop cleanly executing across `test_models.py`, `test_ingestion.py`, and `test_api.py` in 2.22 seconds with zero structural regressions.

### Entry 003: The Move to Radical Reproducibility (Docker Integration)
* **Date & Model:** 2026-01-20 | Gemini 1.5 Pro | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Execution Disparity & Academic Compliance
* **The Technical Challenge:** Minor library updates or variable path mismatches between local environments and cloud instances cause silent formatting failures. For academic peer review (such as targeting a Journal of Open Source Software—JOSS publication), an interactive application must be globally reproducible without external manual installation friction.
* **The Architectural Pivot:** Abandoned traditional cross-platform server setup assumptions. Implemented a containerization protocol via Docker and standard `devcontainer.json` parameters. This configuration ships the exact localized Linux runtime environment alongside the operational source code.
* **Quantitative Milestone:** Repository optimized for automated metadata tracking. Code architecture fully prepared to connect seamlessly with custom domain routing overlays (`thetransparencyproject.me`) and GitHub Pages deployment compilers.

### Entry 004: Portal Refactoring & Repository Standardization
* **Date & Model:** 2026-06-25 | Gemini 3.5 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Frontend Dependency Bloat & Project Standardization Metadata
* **The Technical Challenge:** The portal UI depended on an external Tailwind CDN with a bloated custom configuration injected at runtime. This introduced unnecessary dependency overhead, potential styling glitches upon network latency, and ran counter to local-first, low-overhead open science guidelines. Additionally, project funding and historical tracking lacked standardized registry endpoints.
* **The Architectural Pivot:**
  1. Refactored `index.html` by replacing the Tailwind CDN script and its heavy configuration payload with structured, native CSS custom variables and semantic selectors.
  2. Created `FUNDING.yml` to define repository funding channels (`sothiss` on GitHub and Patreon, `thanks_dev`), ensuring alignment with open-source project compliance.
  3. Established the `JOURNEY.md` log infrastructure to chronologically document key technical decisions, environmental parameters, and milestones.
* **Quantitative Milestone:** Reduced HTML loading dependency footprint from an external multi-megabyte Tailwind engine down to 19 KB of clean, local-first HTML and custom CSS, while keeping the pytest suite fully stable (17/17 tests passing in 0.75s).

### Entry 005: Automated Quality Gates & Adversarial Boundary Verification
* **Date & Model:** 2026-07-08 | Gemini 3.5 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Development Governance, Verification Automation & Dependency Safety
* **The Technical Challenge:** Securing a deterministic data ingestion pipeline requires continuous, machine-enforced verification of prompt constraints, Pydantic type safety, and Darwin Core formatting rules. Furthermore, standard static test assertions cannot dynamically verify biological bounds against infinite combinations of messy narrative inputs, exposing the code to input vulnerability and environment drift.
* **The Architectural Pivot:**
  1. **Pre-Commit Quality Governance:** Implemented a comprehensive `pre-commit` workflow, embedding automated checks using `ruff-format`, `isort`, and `mypy` (with `pydantic` and `pandas-stubs` support) to enforce standard typing rules.
  2. **Custom Domain-Specific Validation Hooks:** Created local hooks to run automated static checks on the codebase, enforcing log level verification (`detect-debug-logs`), prompt validation (`validate-prompts`), temperature boundaries preventing non-deterministic model configurations (`detect-temp-in-prompts`), and Darwin Core schema structure compliance (`validate-dwc-mapping`).
  3. **Adversarial Verification via Property-Based Testing:** Integrated `hypothesis` into the development environment to systematically explore edge-case inputs in `test_adversarial_boundaries.py`, verifying model resilience against invalid heart rates (<30 BPM) and arbitrary narrative injections.
  4. **Deterministic Dependency Auditing:** Wired up `uv` hooks (`uv-add`, `uv-check`, `uv-audit`, and `uv-python-version`) to continuously run package integrity audits, security scans, and environment compliance checks during development.
  5. **Licensing Compliance:** Formally integrated open-source citation metadata by declaring the `MIT` license specification inside `CITATION.cff` and updating `LICENSE` with a clear attribution note.
* **Quantitative Milestone:** Successfully deployed 11 automated pre-commit security, typing, and validation hooks to prevent regression, and expanded the verification suite with property-based testing constraints.

### Entry 006: Credential Isolation, Strict Type Refinement & SAST Scope Control
* **Date & Model:** 2026-07-10 | Gemini 3.5 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type:** Security Hardening, Developer Tooling & Static Analysis Compliance
* **The Technical Challenge:** Integration of observability and dependency hooks introduced three tooling issues:
  1. **Secret Leak & Syntax Errors:** Hardcoding Datadog credentials directly in `pyproject.toml` caused TOML syntax errors and created a security threat of committing active credentials to version control.
  2. **Silent Exceptions & Constructor Mismatches:** Using empty `except` blocks with `pass` in validators masked data errors (flagged as silent exceptions). Redundant `alias` definitions in `MeasurementOrFact` forced type checkers to flag parameter mismatch errors since the constructor names did not match Python variable identifiers. Also, deprecated `datetime.utcnow()` triggered runtime warnings.
  3. **Analysis Noise:** The static analysis engine scanned third-party `.venv` dependencies and local `.env` variables, cluttering output with non-actionable diagnostics.
* **The Architectural Pivot:**
  1. **Secret & Config Separation:** Moved Datadog configuration variables out of `pyproject.toml` into a local git-ignored `.env` file, and kept `pyproject.toml` focused strictly on tooling declarations.
  2. **Validator & Type System Refinement:** Refactored field validators in `models.py` to raise explicit `ValueError` on parsing failure. Removed redundant `alias` declarations on `MeasurementOrFact` to allow standard constructor keyword signatures while preserving validation and serialization aliases. Updated legacy datetimes to use timezone-aware `datetime.now(timezone.utc)`.
  3. **Lint Scope Exclusion:** Added `.venv/` and `.env` to the global `ignore-paths` section in `code-security.datadog.yaml` to restrict static analysis scanning strictly to first-party code.
* **Quantitative Milestone:** Re-established a zero-error and zero-warning developer environment baseline across all first-party modules, fully securing credentials without altering Darwin Core data payloads.

### Entry 007: Solo Maintainer Anti-Bloat Charter & Guardrails Verification Engine
* **Date & Model:** 2026-10-04 | Gemini 3.8 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** Cognitive Budget & Repository Sprawl
* **The Technical Challenge:** As open-source repositories grow, polyglot tooling (Node/npm, Rust, C-extensions), enterprise message brokers (Celery, Redis, Kafka), and out-of-scope cloud skills silently inject cognitive drag and break single-person maintainability.
* **AI Architectural Reasoning & Cognitive Evolution:**
  The AI evaluated the cognitive and operational boundaries of a solo research engineer. Rather than proposing reactive fixes or adding external orchestrators, the model derived five immutable guardrails: (1) Pure Python monoculture (>= 3.11), (2) Dependency budget strictly capped at <= 8 direct packages, (3) Proscription of external daemons and enterprise queue systems, (4) Skill hygiene prohibiting enterprise cloud skills in `.agents/skills`, and (5) Single-command QA enforcement.
* **The Architectural Pivot & Implemented Solution:**
  Built a zero-dependency, automated verification engine in `scripts/audit_maintainer_guardrails.py` and wrapped it in `.\scripts\run_qa.ps1`. The engine executes static AST analysis to detect forbidden language sprawl, parses `pyproject.toml` to guard the 8-dependency cap, scans for prohibited daemons, and audits `.agents/skills/` directory hygiene.
* **Quantitative & Invariant Milestones:** 100% pass across all 5 maintainer guardrail pillars; cognitive line complexity verified under 600 lines per file; audit execution completed in <0.2 seconds.
* **Gemini / AI Evolutionary Note:**
  Demonstrates a significant evolution from 2025 code completion toward systems-level architectural governance: the model autonomously formulated self-limiting guardrails to protect human maintainer bandwidth over multi-year horizons.

### Entry 008: Step-Gated Idea-to-Code Pipeline & Cross-Model Telemetry Handoff
* **Date & Model:** 2026-10-04 | Gemini 3.8 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** Premature Implementation & Cross-Model Context Loss
* **The Technical Challenge:** AI-assisted development often falls victim to "step skipping" (writing code before boundary specifications, typing constraints, and adversarial test definitions are established). Furthermore, switching development across AI model boundaries (Gemini, Claude, GPT, Cursor) causes state fragmentation.
* **AI Architectural Reasoning & Cognitive Evolution:**
  The model identified that disciplined engineering requires strict gating. It structured a 5-gate pipeline (Idea -> Specification -> Test First -> Minimal Code -> QA/Journal) and synthesized telemetry aggregation into a single deterministic script (`scripts/generate_agent_handoff.py`). To remove developer friction, it implemented native PowerShell wrappers (`idea.ps1`, `handoff.ps1`) providing single-stroke terminal workflows.
* **The Architectural Pivot & Implemented Solution:**
  Implemented `scripts/manage_ideas.py` and `scripts/idea.ps1` for auto-generating numbered idea specifications (`docs/ideas/IDEA-XXX_*.md`) with track segregation (`bolt`, `sentinel`, `feat`, `refactor`, `docs`) and automated Kanban board rendering (`docs/IDEAS_BOARD.md`). Paired this with `.\scripts\handoff.ps1` to snapshot git status, test runs, and clipboard handoff blocks.
* **Quantitative & Invariant Milestones:** 5-gate progression mechanically verified via `idea.ps1 -Audit`; live clipboard telemetry generation verified; zero external dependencies introduced.
* **Gemini / AI Evolutionary Note:**
  Highlights Gemini's advanced contextual modeling across complex multi-file workflows without hallucinating configuration keys or violating standard library constraints.

### Entry 009: Institutional Task & Walkthrough Governance and AI Evolution Tracking
* **Date & Model:** 2026-10-04 | Gemini 3.8 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** AI Observability, Reasoning Transparency & Workflow Accountability
* **The Technical Challenge:** In fast-moving AI-pair programming, model reasoning is often opaque. Without structured up-front task decomposition and post-run walkthroughs, the human PI cannot easily audit the cognitive steps, trade-offs, and subtle architectural decisions made during development.
* **AI Architectural Reasoning & Cognitive Evolution:**
  The model addressed the meta-challenge of AI traceability: How do we track how AI reasoning evolves over time (specifically following the PI's exclusive work with Gemini since 2025)? The solution was twofold: (1) Mandate pre-execution micro-task checklists and post-execution walkthroughs in repository rules, and (2) Turn `JOURNEY.md` into an active, easy-to-apply chronicle capturing AI cognitive evolution, paired with dedicated automation (`manage_journey.py` and `journey.ps1`).
* **The Architectural Pivot & Implemented Solution:**
  1. Authored `.agents/rules/walkthrough-and-tasks.md` and integrated the requirement into `AGENTS.md`.
  2. Built `scripts/manage_journey.py` and `scripts/journey.ps1` to provide instantaneous access to blank session-closing templates (`-Template`), entry listings (`-List`), AI evolutionary timeline snapshots (`-Timeline`), and one-command append operations (`-New`).
  3. Structured `JOURNEY.md` with a standardized session closing template and chronological evolutionary logs.
* **Quantitative & Invariant Milestones:** 22/22 unit and adversarial tests passing in 1.04s; 100% maintainer guardrail compliance; `journey.ps1` utility executing instantaneously with zero external dependencies.
* **Gemini / AI Evolutionary Note:**
  Reflects a transition to meta-cognitive engineering where the model actively reflects upon its own cognitive processes, documents architectural rationale, and assists the human researcher in analyzing long-term human-AI co-evolution.

---

## 🛠️ Session Closing / Journey Entry Protocol & Template
To ensure frictionless tracking at the end of every engineering session, use this standardized protocol.

### Quick Start via PowerShell:
```powershell
# 1. Output a fresh template to copy or fill:
.\scripts\journey.ps1 -Template -Title "Your Milestone Title"

# 2. View historical entry timeline and AI model evolution:
.\scripts\journey.ps1 -Timeline
.\scripts\journey.ps1 -List
```

### Standard Session Entry Template:
```markdown
### Entry XXX: [Milestone Title]
* **Date & Model:** YYYY-MM-DD | [e.g. Gemini 3.8 Flash] | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** [Environmental / Architectural / Ingestion / Governance / Security]
* **The Technical Challenge:** [Specific technical friction or constraint encountered]
* **AI Architectural Reasoning & Cognitive Evolution:**
  [Detailed breakdown of how the AI reasoned through the problem: initial mental model, trade-offs evaluated, alternatives rejected, and self-corrections]
* **The Architectural Pivot & Implemented Solution:**
  [Specific code, abstractions, scripts, or architectural patterns introduced]
* **Quantitative & Invariant Milestones:** [Verified test counts, pass rates, benchmark times, guardrails audit results]
* **Gemini / AI Evolutionary Note:**
  [Observations on model behavior: reasoning depth, autonomous fidelity, long-context handling, and human-AI synergy evolution since 2025]
```

---

### Entry 010: Repository Hygiene, GitHub Surface Streamlining & GitBook Sponsorship Unification
* **Date & Model:** 2026-10-04 | Gemini 3.8 Flash | Human PI: Alice Severi Gonçalves
* **Hurdle Type & Problem Space:** Documentation Fragmentation & Clutter Spillover
* **The Technical Challenge:** GitBook Git-Sync generated dummy directories (changelog/, changelog-1/, the-transparecy-project/) and indexed raw repo plumbing into the public documentation sidebar. Meanwhile, our sole sponsor (GitBook) lacked dedicated prominence across documentation headers.
* **AI Architectural Reasoning & Cognitive Evolution:**
  The AI recognized that open-science repositories require a pristine public presentation both on GitHub (sterile root layout, zero empty test directories) and on GitBook (navigable table of contents without internal bot plumbing). The model decoupled internal developer tooling from user-facing documentation in SUMMARY.md, cleaned the multi-space schema in gitbook-docs.yaml to unify EthoPipe into a single root space, and prominently elevated GitBook as our Official Documentation Sponsor across badges and README metadata.
* **The Architectural Pivot & Implemented Solution:**
  Deleted dummy sync directories, unified gitbook-docs.yaml onto a stable single-space configuration, redesigned SUMMARY.md into structured thematic categories (Architecture, Open Science, Governance, Releases), upgraded docs/README.md and docs/releases/README.md into rich indices, and embedded official GitBook documentation badges and acknowledgments.
* **Quantitative & Invariant Milestones:** All 8 QA verification steps passed in 1.26s; pre-commit 100% clean; repository root pruned from 3 extraneous directories to a sterile baseline; GitBook documentation table of contents completely streamlined.
* **Gemini / AI Evolutionary Note:**
  Illustrates Gemini's capability to understand multi-platform ecosystem interactions (GitHub web view vs. GitBook Git-Sync compilation) and autonomously prune artifacts without breaking underlying synchronization schemas or CI/CD pipelines.

---

## 🚀 Active Trajectory & Next Micro-Tasks
- [x] Establish Solo Maintainer Anti-Bloat Charter and automated guardrail auditor (`audit_maintainer_guardrails.py`).
- [x] Implement 5-Gate Idea-to-Code pipeline and automated Kanban board generator (`manage_ideas.py`, `idea.ps1`).
- [x] Standardize cross-model agent handoff engine and automated telemetry copying (`generate_agent_handoff.py`, `handoff.ps1`).
- [x] Codify mandatory Task Deconstruction & Walkthrough rule for all AI agents (`.agents/rules/walkthrough-and-tasks.md`, `AGENTS.md`).
- [x] Build frictionless Journey & AI Evolution management utility (`scripts/manage_journey.py`, `scripts/journey.ps1`).
- [ ] Outline localized storage adapter to safely persist validated Pydantic payloads into a query-optimized dimensional Star Schema.
- [ ] Bind completed JSON Schema validation parameters directly into the Google AI Studio response panel.
