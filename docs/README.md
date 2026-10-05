# EthoPipe Documentation Directory

> **Documentation Sponsor:** Hosted and published via **[GitBook](https://www.gitbook.com/)** under the GitBook Community Plan.

Welcome to the central documentation index for **EthoPipe**, a deterministic, open-science Python ETL pipeline for applied canine ethology and physiological telemetry.

---

## 📚 Documentation Navigation

### 1. Architecture & Biological Specifications
* **[API Ingestion & Webhooks](api-ingestion.md)**: Webhook endpoints, payload formats, and serverless ingestion patterns.
* **[Schema Specifications](SCHEMA.md)**: Kimball Star Schema dimensional modeling, Darwin Core (`dwc:MeasurementOrFact`) mappings, and entity relationships.
* **[Biological Validation](VALIDATION.md)**: Morphology-bounded heart rate thresholds (30–250 BPM) and objective motor sequence enums.

### 2. Open Science, Compliance & Governance
* **[AI Usage Disclosure](ai-usage.md)**: Mechanistic determinism, temperature clamping (`0.0`), and AI code governance.
* **[Open Science Standards](OPEN_SOURCE_STANDARDS.md)**: JOSS, FAIR principles, and OSI licensing compliance.
* **[Solo Maintainer Audit](SOLO_MAINTAINER_AUDIT.md)**: Anti-bloat guardrails, language monoculture (pure Python), and dependency budget (<= 8).
* **[Research & Architecture Journal](../JOURNEY.md)**: Chronological architectural evolution and AI reasoning tracking since 2025.

### 3. Engineering Workflows
* **[Ideas & Task Board](IDEAS_BOARD.md)**: The 5-gate pipeline (Idea -> Spec -> Test -> Code -> Done) tracking active proposals.
* **[Cross-Model Agent Handoff](AGENT_HANDOFF_WORKFLOW.md)**: Lossless telemetry and state synchronization across AI models.
* **[Code Companion Workflow](CODE_COMPANION_WORKFLOW.md)**: Delegation guidelines and journal maintenance for autonomous bots (Jules).

### 4. Releases
* **[Releases Directory](releases/README.md)**: Versioned changelogs and release notes.
* **[Full Changelog](../CHANGELOG.md)**: Chronological commit and release log.
