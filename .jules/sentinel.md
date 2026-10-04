## 2026-09-08 - Subject ID Length Boundary Hardening in CanineObservation Model
**Learning:** Unbounded string inputs for `subject_id` expose the ingestion pipeline to potential denial-of-service, memory bloat, and cache-poisoning payloads during high-throughput field telemetry ingestion.
**Action:** Enforce strict `max_length=64` on `subject_id` in Pydantic v2 schemas (`src/pipeline/models.py`) accompanied by adversarial length validation tests in `tests/test_models.py`.
