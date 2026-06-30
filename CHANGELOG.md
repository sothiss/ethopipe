# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
