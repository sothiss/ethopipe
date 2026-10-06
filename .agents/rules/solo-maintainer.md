---
trigger: always_on
---

# Solo Maintainer Guardrails & Anti-Bloat Invariants

EthoPipe is maintained by a solo research software engineer. To ensure long-term sustainability, reliability, and low cognitive friction, all AI agents, code companions (Jules), and contributors MUST adhere to these non-negotiable guardrails:

## 1. Absolute Language Monoculture
- **100% Python**: Core application code, data extraction, and pipelines must be written in Python (>= 3.11).
- **Prohibited Languages & Tools**: Never introduce Node.js, npm, TypeScript, React, Go, Rust, or C/C++ build steps.
- **Self-Contained Web Demos**: Any web demos (e.g. `index.html`) must be standalone, vanilla HTML/CSS/JS without npm packaging, bundlers, or frameworks.

## 2. Dependency Budget & Anti-Sprawl
- **Budget**: Direct runtime dependencies in `pyproject.toml` are capped at **<= 8** packages.
- **Stdlib Priority**: Always prefer Python's standard library (`pathlib`, `tomllib`, `dataclasses`, `argparse`, `typing`, `sqlite3`) over adding third-party packages.
- **Prohibited Dependencies**: Never introduce external daemons (Redis, Celery, RabbitMQ), heavyweight machine learning frameworks (PyTorch, TensorFlow, PySpark), or enterprise workflow managers (Airflow).

## 3. Skill & Plugin Hygiene
- Do NOT install or copy enterprise cloud data platform skills (GCP Composer, BigQuery DTS, Dataproc Spark, Dataform, Lakehouse) into this repository's `.agents/skills`.
- Workspace skills are strictly limited to core engineering quality (`code-quality`, `code-companion`, `agent-handoff`, `sync-node`, `managing-python-dependencies`).

## 4. Architectural Simplicity (KISS & YAGNI)
- Keep EthoPipe as a single modular Python service (FastAPI + Supabase).
- Individual files must remain under 600 lines.
- One single command executes the entire verification pipeline: `.\scripts\run_qa.ps1` or `python scripts/audit_maintainer_guardrails.py`.
