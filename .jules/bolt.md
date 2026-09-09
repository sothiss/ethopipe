## 2026-03-30 - Pre-computed Enum Lookups for Pydantic Field Validators
**Learning:** Iterating through enum members (especially multi-member StrEnum types) inside Pydantic field validators causes an O(N) linear scan and repeated string allocations (`.lower()`) on every parsed field, creating a major bottleneck in ingestion pipelines.
**Action:** Pre-build module-level lookup dictionaries (`_EXACT_LOOKUP` and `_LOWER_LOOKUP`) at import time to achieve O(1) validator performance without breaking Enum validation compatibility.
