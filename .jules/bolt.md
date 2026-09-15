## 2026-07-06 - Fast Substring Pre-Check Before Regex Searching in Model Field Validators
**Learning:** In field validators running on large volumes of valid text notes (~99%+ containing no prohibited terms), compiling a regex and executing `re.search()` on every string incurs high regex engine setup and matching overhead.
**Action:** Use a fast C-level substring check (`any(w in text_lower for w in PROHIBITED_WORDS_TUPLE)`) to short-circuit regex searches for clean text, reducing validation overhead by ~75% (~4x speedup).

## 2026-07-05 - O(1) Dictionary Lookup vs Enum Iteration in Pydantic Field Validators
**Learning:** Custom field validators that perform linear scans over StrEnum members (`for member in Enum: ...`) introduce severe overhead (~170x slower for 38 members) due to repeated string allocations and `.lower()` comparisons during high-volume Pydantic payload deserialization.
**Action:** Pre-compute a module-level dictionary mapping (`_LOOKUP`) for enum names, values, and lowercased variants to convert enum field parsing to an O(1) hash table lookup.
