## 2026-07-05 - Pre-computed Enum Lookup Dict for Pydantic Field Validators

**Learning:** Pydantic custom `@field_validator` functions that iterate over enum members and perform lowercasing (`member.name.lower()`, `member.value.lower()`) on every input validation introduce substantial overhead (~150x slower) compared to module-level dictionary lookups.
**Action:** Always pre-compute a module-level dictionary mapping string representations and lowercased string keys to Enum instances for O(1) field validation.
