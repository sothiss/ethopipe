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
* **Hurdle Type:** Environmental Anomalies & Git History Friction
* **The Technical Challenge:** The local development environment was suffering from compounding configuration debt. Bloated IDE extensions (Azure/Kubernetes proxies) were polluting execution paths, while raw Google Cloud Application Default Credentials (ADC) endpoints were misaligned. The local version control history had devolved into volatile tracking cycles.
* **The Architectural Pivot:** Performed an explicit "intellectual garbage collection." 
  1. Ruthlessly pruned the IDE extension panels to maximize processing bandwidth.
  2. Executed an operational Git reset to eliminate tracking clutter and establish a sterile repository baseline.
  3. Re-authenticated cloud credentials globally via `gcloud auth application-default login` outside the immediate codebase paths.
* **Quantitative Milestone:** A pristine, standardized root repository structure (`src/`, `tests/`, `docs/`) deployed safely to a single tracking line on `main` at `github.com/sothiss/ethopipe`.

### Entry 002: Hardcoding Biological Realities into the Pydantic Matrix
* **Hurdle Type:** Semantic Ingestion Bias vs. Deterministic Gatekeeping
* **The Technical Challenge:** Unstructured field narratives and handler logs contain high frequencies of anthropomorphic, subjective terms (e.g., "Max was being stubborn and protective"). Furthermore, manual data entries introduce extreme physiological anomalies that can corrupt downstream quantitative analytical engines.
* **The Architectural Pivot:** Translated paper-based canine behavior literature (Hsu & Serpell's C-BARQ parameters, Bekoff, Handelman, and 2024 peer-reviewed ethograms) directly into immutable Python code blocks. Hardcoded biological guardrails into Pydantic models:
  * Restricting viable heart rates strictly between $30$ and $250$ BPM (flagging anomalous values like 380 or 400 BPM as immediate `ValidationError` exceptions).
  * Coercing behavioral observations strictly into validated Enums (`play_bow`, `licking_of_lips`, `looking_away`, `posture_freeze`).
* **Quantitative Milestone:** Successfully built and verified a 43-test passing validation validation loop cleanly executing across `test_models.py`, `test_ingestion.py`, and `test_api.py` in 2.22 seconds with zero structural regressions.

### Entry 003: The Move to Radical Reproducibility (Docker Integration)
* **Hurdle Type:** Execution Disparity & Academic Compliance
* **The Technical Challenge:** Minor library updates or variable path mismatches between local environments and cloud instances cause silent formatting failures. For academic peer review (such as targeting a Journal of Open Source Software—JOSS publication), an interactive application must be globally reproducible without external manual installation friction.
* **The Architectural Pivot:** Abandoned traditional cross-platform server setup assumptions. Implemented a containerization protocol via Docker and standard `devcontainer.json` parameters. This configuration ships the exact localized Linux runtime environment alongside the operational source code.
* **Quantitative Milestone:** Repository optimized for automated metadata tracking. Code architecture fully prepared to connect seamlessly with custom domain routing overlays (`thetransparencyproject.me`) and GitHub Pages deployment compilers.

### Entry 004: Portal Refactoring & Repository Standardization
* **Hurdle Type:** Frontend Dependency Bloat & Project Standardization Metadata
* **The Technical Challenge:** The portal UI depended on an external Tailwind CDN with a bloated custom configuration injected at runtime. This introduced unnecessary dependency overhead, potential styling glitches upon network latency, and ran counter to local-first, low-overhead open science guidelines. Additionally, project funding and historical tracking lacked standardized registry endpoints.
* **The Architectural Pivot:** 
  1. Refactored `index.html` by replacing the Tailwind CDN script and its heavy configuration payload with structured, native CSS custom variables and semantic selectors.
  2. Created `FUNDING.yml` to define repository funding channels (`sothiss` on GitHub and Patreon, `thanks_dev`), ensuring alignment with open-source project compliance.
  3. Established the `JOURNEY.md` log infrastructure to chronologically document key technical decisions, environmental parameters, and milestones.
* **Quantitative Milestone:** Reduced HTML loading dependency footprint from an external multi-megabyte Tailwind engine down to 19 KB of clean, local-first HTML and custom CSS, while keeping the pytest suite fully stable (17/17 tests passing in 0.75s).

---

## 🚀 Active Trajectory & Next Micro-Tasks
- [ ] Bind the completed JSON Schema validation parameters directly into the Google AI Studio response panel.
- [ ] Clamp `gemini-2.5-pro` parameter execution thresholds to a temperature of strict `0.0` to force the AI to function purely as a constrained text-cleaning clerk.
- [ ] Outline a localized storage adapter to safely persist validated Pydantic payloads into a query-optimized dimensional Star Schema structure.