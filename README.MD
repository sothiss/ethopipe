# EthoPipe: ETL Pipeline for Applied Canine Ethology

Open-science ethological data ingestion pipeline for structured, reproducible behavioral data collection and validation.

## Overview
This project aims to support reproducible ethological research by validating, normalizing, and ingesting structured observational data through a deterministic Python-based pipeline.

## Features
- Pydantic-based schema validation
- FastAPI ingestion endpoints
- Testable Python package structure
- Open-source repository with reproducible setup

## Project status
Early rebuild / MVP

## Documentation and Specifications
We have extensive documentation, research papers, and architectural specifications available in the `docs/` directory:
- `docs/specifications/`: Technical and architectural specifications.
- `docs/research_papers/`: Research papers and ethogram definitions.
- `docs/whitepapers/`: Whitepapers and concept documents.
- `docs/misc/`: Additional resources.

## Installation

We recommend using a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Contributing

We welcome contributions! Please refer to the `CONTRIBUTING.md` file for details on how to set up your environment, our code standards, and the pull request process.

## Repository structure

- `src/` - Application code
- `tests/` - Automated tests
- `docs/` - Project documentation, specifications, and papers
- `.github/workflows/` - CI/CD pipelines

## Author
Alice Severi Gonçalves

ORCID: https://orcid.org/0009-0003-0048-8982

## License

This project is distributed under the terms of the LICENSE file.
