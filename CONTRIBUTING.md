# Contributing to EthoPipe

Welcome to the EthoPipe project! We are thrilled that you'd like to contribute to this open-science ethological data ingestion pipeline.

Our goal is to build a structured, reproducible behavioral data collection and validation tool, and we welcome contributions from developers, researchers, and ethologists alike.

## Ways to Contribute

There are many ways you can help:
- **Code Contributions:** Implement new features, fix bugs, or improve the project infrastructure.
- **Documentation:** Enhance our README, add docstrings, or write tutorials.
- **Research & Validation:** Help refine the canine ethogram operational definitions and ensure they align with veterinary parameters.
- **Issue Reporting:** Found a bug? Open an issue on our tracker.

## Setting Up for Development

We require a few tools to ensure code quality and reproducibility.

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/sothiss/EthoPipe.git
   cd EthoPipe
   ```

2. **Set up a Virtual Environment:**
   Set up your preferred virtual environment (e.g. venv, conda).

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install Pre-commit Hooks:**
   We use `pre-commit` to run Black and Ruff on every commit to maintain consistent code formatting and quality.
   ```bash
   pre-commit install
   ```

## Development Guidelines

- **Determinism is Key:** We aim for strict schema validation. All features should be deterministic and reproducible.
- **Pydantic Strict Mode:** For new/updated Pydantic models, set `model_config = ConfigDict(strict=True)` (Pydantic v2).
- **Testing:** We practice test-driven development. Ensure any new feature includes adequate test coverage in the `tests/` directory. Run tests locally using `pytest`:
  ```bash
  pytest tests/
  ```
- **Code Formatting:** Our pre-commit hooks will automatically format your code with Black and lint it with Ruff.

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit your changes. Ensure pre-commit checks pass!
3. Push to your branch: `git push origin feature/your-feature-name`
4. Open a Pull Request (PR) on GitHub.

Our Continuous Integration (CI) pipeline will run on your PR. Make sure all checks pass before requesting a review.

## Code of Conduct

Please treat all members of the community with respect. We foster a collaborative, open-science environment where constructive feedback is encouraged.

Thank you for contributing!
