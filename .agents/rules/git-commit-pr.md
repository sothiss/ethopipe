---
trigger: always_on
---

# Git Commit & Pull Request Standards (Solo Maintainer Edition)

All commits, branches, and Pull Requests in the EthoPipe repository MUST follow these solo-maintainer patterns. Before committing or opening a Pull Request, synchronize workspace state via `sync-node` and verify compliance with `solo-maintainer-audit` and `code-quality` (and `release-governance` when cutting releases).

## 1. Pragmatic Solo-Maintainer Branching Policy
Because EthoPipe is maintained by a single Principal Investigator (`@sothiss`), **creating a branch and PR for every routine commit is NOT required**:

- **Direct to `main` (Fast Path — Allowed for Solo Owner):**
  - Routine documentation, `JOURNEY.md` entries, `docs/PROJECT_STATE.md` checkpoints, `docs/IDEAS_BOARD.md` updates, `.agents/` rules/skills, `scripts/` helpers, static site updates (`index.html`), version release commits, and small atomic fixes **provided local pre-commit / QA checks already pass**.
- **Semantic Branch + PR (`<prefix>/<scope>-<kebab-case-topic>` — Required When):**
  1. Making multi-commit features, breaking refactors, or high-risk schema/parser/API changes (`src/pipeline/models.py`, `parser.py`, `api.py`) that benefit from isolated testing or easy rollback.
  2. Delegating work to an **autonomous background agent / subagent** or external contributor (**autonomous bots must NEVER commit or push directly to `main`**).
  3. Reviewing grouped dependency updates (e.g., monthly Dependabot PRs).
- **Standard Branch Prefixes (when branching):**
  - `feature/<scope>-<feature-name>` (`track:feature` — Schema, Darwin Core mapping, FastAPI pipeline, parser, telemetry UI)
  - `fix/<scope>-<issue-name>` (Bug fixes, validation or boundary regressions)
  - `perf/bolt-<optimization-name>` (`track:bolt` — Performance, caching, vectorization)
  - `security/sentinel-<hardening-name>` (`track:sentinel` — Security, input sanitization, boundary defense)
  - `refactor/<scope>-<topic>` (`track:refactor` — Simplification, modularization, `< 600` line enforcement)
  - `docs/<scope>-<doc-name>` / `test/<scope>-<test-name>` / `chore/<scope>-<task-name>`

## 2. Directory-to-Scope Commit Pattern (Conventional Commits)
Whether committing to `main` or a branch, format every commit header as:
`<type>(<scope>): <imperative lowercase summary>` (max 72 characters)

- **Allowed `<type>` values:** `feat`, `fix`, `perf`, `docs`, `refactor`, `chore`, `test`
- **Canonical `<scope>` mapped from modified directory:**
  - `src/pipeline/` (`api.py`, `main.py`, `models.py`, `parser.py`) -> `pipeline` (or `schema` for pure Pydantic/DwC model changes)
  - `src/pipeline/agent.py` -> `agent`
  - `src/utils/` -> `utils`
  - `tests/` -> `tests`
  - `index.html`, `ethopipe/index.html`, `the-project/`, `assets/`, `logo*.svg` -> `web`
  - `scripts/` -> `scripts`
  - `docs/`, `JOURNEY.md`, `DESIGN.md`, `CHANGELOG.md`, or root markdown -> `docs` (or `state` / `ideas` for checkpointing)
  - `pyproject.toml`, `uv.lock`, `requirements.txt` -> `deps` (or `release` when bumping versions with `CITATION.cff`)
  - `.github/`, `.devcontainer/`, `Dockerfile`, `compose.yaml`, `.pre-commit-config.yaml` -> `ci` or `infra`
  - `.agents/`, `AGENTS.md` -> `rules` or `skills` (e.g., `chore(rules): ...`, `chore(skills): ...`)
- Keep commits atomic by directory and concern. Do not bundle unrelated changes into a single commit.

## 3. Pre-Commit Safety & Governance Gate
Before running `git commit`:
- **Secret Hygiene:** Verify zero plaintext secrets, API keys (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `DD_API_KEY`, `SENTRY_DSN`), or `.env` files are staged.
- **Protected Shared & Sync Files:** Verify canonical governance and GitBook-synced files (`README.md`, `LICENSE`, `CITATION.cff`, `.gitignore`, `.env.example`, `SUMMARY.md`, `gitbook-docs.yaml`) were not altered without explicit instruction.
- **Solo Maintainer & Scientific Invariants:**
  - Verify 100% pure Python (`>= 3.11`), `<= 8` direct runtime dependencies in `pyproject.toml`, a synchronized `uv.lock`, zero unauthorized foreign runtimes/daemons, and `< 600` lines per file in `src/`.
  - Verify deterministic ethological invariants hold: `temperature=0.0`, Pydantic `ConfigDict(strict=True)`, canine heart rate clamped to `[30, 250]` BPM, and Darwin Core (`MeasurementOrFact` / `basisOfRecord`) fidelity.
- **Automated Checks:** Ensure pre-commit hooks (`ruff`, `mypy`, prompt/DwC validators, `uv lock --check`) and `python scripts/audit_maintainer_guardrails.py` pass when code, scripts, or dependencies were modified.

## 4. Pull Request Standard (When Using Branches)
- **PR Title:** Must match Conventional Commits format (`<type>(<scope>): <summary>`).
- **PR Body:** Must use `.github/pull_request_template.md` with summary, selected track (`bolt`, `sentinel`, `feature`, `refactor`, or `maintainer`), verification command proof, and completed quality gates (`CHANGELOG.md` / `JOURNEY.md` where applicable).
