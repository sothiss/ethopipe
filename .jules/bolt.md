## 2026-07-05 - O(1) Dictionary Lookup vs Enum Iteration in Pydantic Field Validators
**Learning:** Custom field validators that perform linear scans over StrEnum members (`for member in Enum: ...`) introduce severe overhead (~170x slower for 38 members) due to repeated string allocations and `.lower()` comparisons during high-volume Pydantic payload deserialization.
**Action:** Pre-compute a module-level dictionary mapping (`_LOOKUP`) for enum names, values, and lowercased variants to convert enum field parsing to an O(1) hash table lookup.

## 2026-07-05 - Zero-Allocation Early Returns via re.Pattern.subn()
**Learning:** Performing unconditional `re.sub()` followed by secondary regex whitespace normalization and string stripping on free-text inputs creates unnecessary string allocations and regex passes for clean text (~100% of non-violating payloads). Using `re.Pattern.subn()` provides the substitution count in a single pass; when `count == 0`, returning the input string directly avoids all subsequent regex and allocation overhead (~46% faster for `de_bias_text`, ~23% faster for full payload normalization).
**Action:** Use `subn()` to obtain substitution counts and bypass secondary text cleanup pipelines when zero replacements occur.
