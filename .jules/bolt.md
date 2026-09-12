## 2026-07-05 - O(1) Dictionary Lookup vs Enum Iteration in Pydantic Field Validators
**Learning:** Custom field validators that perform linear scans over StrEnum members (`for member in Enum: ...`) introduce severe overhead (~170x slower for 38 members) due to repeated string allocations and `.lower()` comparisons during high-volume Pydantic payload deserialization.
**Action:** Pre-compute a module-level dictionary mapping (`_LOOKUP`) for enum names, values, and lowercased variants to convert enum field parsing to an O(1) hash table lookup.
