# EthoPipe: An Open-Science ETL Pipeline for Applied Canine Ethology and Physiological Telemetry

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![CI/CD Pipeline](https://github.com/sothiss/ethopipe/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21211371-blue)](https://doi.org/10.5281/zenodo.21211371)
[![ORCID iD](https://img.shields.io/badge/ORCID-0009--0003--0048--8982-green)](https://orcid.org/0009-0003-0048-8982)

An open-access biological informatics pipeline developed under **The Transparency Project** (`thetransparencyproject.me`).

---

## 🔬 1. Statement of Need & Scientific Purpose

Within applied animal behavior and canine ethology, researchers face a critical data bottleneck: ground-level field observations, shelter logs, and handler incident reports are heavily trapped within fragmented, qualitative, and highly subjective text narrative silos. Human observers frequently introduce significant inter-rater variance by projecting anthropomorphic storytelling or cultural functional interpretations onto animals (e.g., qualifying a canine subject's internal state as "angry," "guilty," or "stubborn" instead of documenting objective, observable physical motor sequences). 

Because these qualitative data lack uniform formatting and objective operational baselines, they are mathematically unviable for population-scale continuous multi-center epidemiological studies, multi-way statistical models, or rigorous quantitative peer review. This systemic deficit in data engineering directly fuels a replication crisis across the companion animal welfare space.

EthoPipe resolves this crisis by introducing a programmatic digital gatekeeper. It operates as a Python-based Extract, Transform, Load (ETL) pipeline and web API that normalizes unstructured handler prose into deterministic, machine-readable datasets. Shifting the paradigm away from subjective storytelling, EthoPipe builds the standardized, population-scale data infrastructure necessary for veterinary behaviorists and epidemiologists to reliably extract verifiable statistical correlations between environmental interventions and objective behavioral or physiological outcomes.

---

## 🛠️ 2. Core Architecture & Technical Specifications

To enforce absolute reproducibility and data integrity, the pipeline completely decouples its semantic parsing from downstream evaluation and serialization layers across three operational phases:

[Qualitative Narrative] ──> [Gemini 2.5 Pro Parser] ──> [Strict Pydantic Validation] ──> [Darwin Core (DwC) Mapping]
(Messy Handler Notes)       (Clamped Temp: 0.0)         (Type Enforced Bounds)     (Global Data Interop)


1. **Semantic Parsing (Extract):** Ingests raw text strings utilizing the advanced `gemini-2.5-pro` architecture. By locking the model's generation temperature parameter strictly to absolute zero (`0.0`) and activating structured JSON output configurations backed by schema exports, the model is stripped of creative expression. It functions strictly as a deterministic text-cleaning clerk, mapping qualitative human prose down to typed key-value records while leaving the context window immune to stochastic variance or hallucinations.
2. **Type Enforcement Matrix (Transform):** Intercepted arrays pass directly into localized Pydantic validation models configured with `ConfigDict(strict=True)`. This engine acts as an unyielding filter that hardcodes biological and morphological constraints derived directly from published veterinary literature—such as mathematically restricting canine heart rate inputs strictly between `30` and `250 BPM` (derived from the *Merck Veterinary Manual*). Any entries containing non-scientific designations, string typos, or malformed data are instantly rejected at the gate and routed to a background quarantine queue.
3. **Biological Informatics Integration (Load):** Natively aligns verified internal variables with international **Darwin Core (DwC)** metadata schemas to maintain seamless interoperability with global biodiversity informatics platforms (such as GBIF and OBIS):
   * Internal subject identifiers map straight to `dwc:individualID`.
   * Temporal vectors utilize strict ISO 8601 formatting under `dwc:eventDate`.
   * Explicit behavioral categories assign to `dwc:measurementType` (e.g., `'play_bow'`, `'licking_of_lips'`, `'panting'`).
   * Categorical frequencies or durations assign to `dwc:measurementValue`.
   * Methodological classifications leverage `dwc:basisOfRecord`, cleanly segregating human visual coding logs (`HumanObservation`) from telemetry ingested directly from physical sensors (`MachineObservation`).

Finalized structures are organized into a query-optimized relational **Star Schema**, ensuring clean dimensionality for advanced multidimensional testing (ANOVA, Chi-Square tests of independence) in Pandas or R.

---

## 🤖 3. Continuous Integration & Code Guardrails

To preserve code health and protect against dependency drift ("bit rot") over long-term research cycles, this repository enforces a rigorous, multi-stage automated Continuous Integration (CI) engine via GitHub Actions (`.github/workflows/ci.yml`) on every code push or pull request to the `main` branch:

1. **`lint` (Programmatic Styling & Hygiene Gate):** * Validates absolute style consistency using the `Black` formatting check suite across your files.
   * Statically reviews syntax anomalies and code smells using the high-velocity `Ruff` linter tool.
2. **`tests` (Functional Regression Gate):**
   * Spins up isolated execution environments across a matrix of Python `3.11` and `3.12`.
   * Runs our comprehensive testing layer via `pytest`, executing your verified test cases to ensure edge-case mutations or invalid telemetry boundaries are caught before deployment.
   * Compiles code coverage metrics via XML reports linked cleanly to Codecov trackers.
3. **`schema-validation` (Ontological Drift Gate):**
   * Runs dedicated structural testing to confirm modifications do not introduce silent drift to core data dictionaries.

---

## 🎯 4. Workspace Roadmap (GitHub Projects Integration)

Development progress is tracked natively on our automated Kanban workspace board. Tasks are sequenced to prioritize structural data ontology before scaling production endpoints:

### 📦 Milestone 1: Core Engine & Legal Foundations [Completed]
* [x] **Task 1:** Codify strict Pydantic validation schemas with `ConfigDict(strict=True)` in `src/models.py` to handle type enforcement and biological baselines.
* [x] **Task 2:** Deploy a formal, plain-text `LICENSE.txt` file into the repository root directory to establish our open-science legal framework.

### 🤖 Milestone 2: Automation & Ingestion Middleware [In Progress]
* [ ] **Task 3:** Optimize the GitHub Actions multi-version execution matrix and configure required status merge gates.
* [ ] **Task 4:** Complete the semantic data extraction module inside `src/prompts.py` using clamped zero-temperature Google SDK structured output configurations.

---

## 💰 5. Open-Science Infrastructure Grants (Sponsorship Tiers)

Maintaining an unfiltered, independent scientific data infrastructure demands active computational resources. Your financial support directly subsidizes the high-volume token throughput fees of advanced model parsing runs, serverless cloud backends, and live database persistence blocks required to keep this library universally accessible.

If you match our criteria or wish to support computational animal welfare, back our development footprint via the repository sidebar sponsor button across these three optimized tiers:

* 🥉 **Tier 1: Empirical Observer (`$5.00` / month):** Tailored for companion animal guardians, student ethologists, and civilian scientists. Grants read-only viewing permissions for live data tracking matrices and monthly *Research-in-Brief* digests decoding complex canine literature.
* 🥈 **Tier 2: Computational Ethologist (`$15.00` / month):** Tailored for independent developers, data scientists, and veterinary behavior technicians. Grants direct access to pre-built Python code snippets, JSON Schema modules, Pydantic templates, and an invite to our private Discord channel for prompt tuning.
* 🥇 **Tier 3: Principal Investigator (`$50.00` / month):** Tailored for academic researchers, institutional clinics, and enterprise AI architects. Grants production-ready Gemini system instructions, quarter-scale pipeline code-review audits, and custom data rule mapping to Darwin Core standards.

---

## 🪪 6. Academic Identity & Permanent Records

* **Principal Systems Architect:** Alice Severi Gonçalves
* **ORCID Persistent Scientific iD:** [0009-0003-0048-8982](https://orcid.org/0009-0003-0048-8982)
* **Archive Software Deposit (DOI):** [10.5281/zenodo.21211371](https://doi.org/10.5281/zenodo.21211371)
* **Live Informatics Directory:** [thetransparencyproject.me](https://thetransparencyproject.me)

### 🤝 Infrastructure Acknowledgements & Grants-in-Kind
This open-science research tool is made possible through infrastructure provisions and developer platform subsidies graciously supplied by the following organizations:
* **GitHub Education / Student Developer Pack:** Providing automated continuous integration pipeline allocations, containerized sandbox hosting boundaries, and environment protection configurations.
* **Google Cloud & Google Developers Program:** Subsidizing compute resource token allocations for advanced large language model parsing within Google AI Studio.
* **NVIDIA Developer Program:** Granting entry-level developer network access and compute engineering frameworks for future computer-vision analytical testing passes.
* **GitBook Community Plan:** Supporting open-science communication by providing specialized access to team compilation engines to maintain our public technical specifications directory.

### 📝 Grounding Bibliography
1. **Broseghini, A., Lõoke, M., Guérineau, C., Marinelli, L., & Paolo Mongillo. (2024).** Ethogram of the predatory sequence of dogs (Canis familiaris). *Applied Animal Behaviour Science*, 279, 106402. [https://doi.org/10.1016/j.applanim.2024.106402](https://doi.org/10.1016/j.applanim.2024.106402)
2. **de Winkel, T., van der Steen, S., Enders-Slegers, M. J., Griffioen, R., Haverbeke, A., Groenewoud, D., & Hediger, K. (2024).** Observational behaviors and emotions to assess welfare of dogs: A systematic review. *Journal of Veterinary Behavior*, 72, 1-17. [https://doi.org/10.1016/j.jveb.2023.12.007](https://doi.org/10.1016/j.jveb.2023.12.007)
3. **Merck Veterinary Manual.** *Normal Physiological Values for Dogs.*
