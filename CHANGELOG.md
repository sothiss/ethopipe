# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-10-04

### Added
- Automated package release workflow (`.github/workflows/release.yml`) triggered on semantic tags (`v*.*.*`), building sdist/wheel distributions, generating SHA256 checksums, and creating GitHub Releases.
- Standardized GitHub Issue Forms (`.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, `maintenance.yml`) with structured dropdowns and validation.
- Standardized Pull Request template (`.github/pull_request_template.md`) enforcing Solo Maintainer quality gates and track classifications (`bolt`, `sentinel`, `feature`, `refactor`, `maintainer`).
- Solo Maintainer Guardrails audit engine (`scripts/audit_maintainer_guardrails.py`) and JOSS / FAIR Open Science compliance verification engine (`scripts/verify_open_source_standards.py`).
- Automated multi-model context switching and agent handoff automation (`scripts/generate_agent_handoff.py`).
- Architectural Journey and AI reasoning history logging (`JOURNEY.md` and `scripts/manage_journey.py`).
- Grouped Dependabot updates (`.github/dependabot.yml`) for `pip` (`core-dependencies`, `dev-dependencies`) and `github-actions` to eliminate multi-PR alert fatigue.

### Changed
- Streamlined CI workflow (`.github/workflows/ci.yml`) by eliminating redundant test jobs, upgrading actions to `@v7`, and embedding automated Mypy type-checking and Solo Maintainer guardrail gates.
- Updated `actions/labeler` workflow to `@v5`.
- Updated GitHub Pages deployment workflow to use `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4`.
- Upgraded project dependencies and locked in deterministic `uv.lock`.

### Security
- Verified zero CVE vulnerabilities with `uv audit` across Python dependencies.
- Added strict Pydantic v2 input validation with canine physiological bounds clamping ([30, 250] BPM).

### Added
- Split GitHub CI workflow into separate status checks: `lint`, `tests`, and `schema-validation`.
- Updated `.gitignore` to block accidental commits of credentials and keys (`*.key`, `*.pem`, `secrets.*`, `credentials.*`).
- Configured `.github/CODEOWNERS` with rules mapping scientific-validity modules, schema specifications, and test fixtures to the lead developer.
- Created `CODE_OF_CONDUCT.md` in the repository root.
- Created `docs/ai-usage.md` documenting guidelines and disclosures for AI coding assistance.
- Created `docs/schema.md` detailing the ethological incident data models and constraints.
- Created `docs/validation.md` detailing strict validation parameters, veterinary physiological boundaries, and Darwin Core mapping.

## [0.1.0] - 2026-06-30

### Added
- Initial project structure for the early EthoPipe rebuild.
- Basic Pydantic models for `EthologicalIncident` validation.
- FastAPI ingestion endpoints with basic authentication.
- Initial test suite for models and ingestion endpoints.
