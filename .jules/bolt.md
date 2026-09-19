## 2026-07-05 - O(1) Dictionary Lookup vs Enum Iteration in Pydantic Field Validators
**Learning:** Custom field validators that perform linear scans over StrEnum members (`for member in Enum: ...`) introduce severe overhead (~170x slower for 38 members) due to repeated string allocations and `.lower()` comparisons during high-volume Pydantic payload deserialization.
**Action:** Pre-compute a module-level dictionary mapping (`_LOOKUP`) for enum names, values, and lowercased variants to convert enum field parsing to an O(1) hash table lookup.

## 2026-07-05 - Fast-Path Presence Checks Before Regex Substitutions in Text Sanitization
**Learning:** Unconditionally invoking `pattern.sub()` and re-compiling uncompiled regexes (`re.sub(r"\s+", ...)`) during text sanitization causes significant overhead on clean strings.
**Action:** Use `pattern.search(text)` and C-fast string presence checks (`'  ' in text`, `'\t' in text`, etc.) before executing regex substitutions, and pre-compile regexes at module level.
