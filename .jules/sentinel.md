## 2026-07-05 - Unbounded Free-Text & Collection DoS Mitigation
**Vulnerability:** Free-text string fields (`location`, `context_session`, `additional_notes`) and collection lists (`behaviors`) in `CanineObservation` models lacked explicit `max_length` bounds, exposing the pipeline to CPU/memory exhaustion (DoS) when parsing or regex-filtering large payloads.
**Learning:** Pydantic models require explicit `max_length` constraints on string and collection fields to prevent ReDoS and memory consumption attacks during input validation and regex checks.
**Prevention:** Always define `max_length` on `Field(...)` for user-supplied string and list attributes in API request models.
