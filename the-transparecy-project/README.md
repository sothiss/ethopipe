---
description: Open-science ETL for canine ethology and physiological telemetry.
---

# Page

## EthoPipe

EthoPipe converts field notes, shelter logs, and incident reports into structured datasets.

It supports reproducible canine-behavior research and physiological telemetry analysis.

### Pipeline

1. **Extract** — Parse narrative observations into typed records.
2. **Transform** — Validate records against biological and morphological limits.
3. **Load** — Map verified data to Darwin Core metadata fields.

The pipeline uses strict Pydantic validation to reject malformed values.

### Data principles

Record observable motor sequences. Avoid inferred emotional states or cultural interpretations.

Use ISO 8601 timestamps and stable subject identifiers. Separate human observations from machine telemetry.

### Project resources

* [Source code](https://github.com/sothiss/ethopipe)
* [Software archive](https://doi.org/10.5281/zenodo.21211371)
* [Research directory](https://thetransparencyproject.me)
