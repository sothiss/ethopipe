# EthoPipe Validation Specification

This document details the validation constraints and mappings enforced by the EthoPipe data pipeline. All observational inputs must satisfy these criteria to be accepted into the data store.

---

## 1. Schema Validation (Pydantic v2)
Every ingestion endpoint enforces Pydantic v2 schemas executing under strict mode configurations:
```python
model_config = ConfigDict(strict=True)
```
Any implicit type coercion (e.g., parsing a string `"80"` into an integer `80` or accepting malformed UUID strings) is rejected at the deserialization boundary to preserve datatype precision.

---

## 2. Veterinary Physiological Clamping
To prevent corrupted entries or data contamination, physiological metrics must comply with peer-reviewed veterinary benchmarks (Merck Veterinary Manual):

### Canine Heart Rate (`heart_rate_bpm`)
The absolute boundaries for canine heart rates are clamped strictly:
- **Absolute Minimum:** `30` BPM
- **Absolute Maximum:** `250` BPM

Additionally, if size classification metadata is present, the following size-dependent parameters apply:
- **Toy Breeds (e.g., Chihuahua, Pomeranian):** Bounded strictly between `80` and `200` BPM.
- **Giant Breeds (e.g., Great Dane, Mastiff):** Bounded strictly between `40` and `110` BPM.

### Respiration Rate (`resp_rate_bpm`)
- **Valid Range:** `10` to `120` breaths per minute.

### Core Body Temperature (`body_temp_c`)
- **Valid Range:** `36.0` to `41.5` °C.

### Cortisol Biomarkers (`cortisol_nmolL`)
- **Biomarker:** Salivary and serum Cortisol concentrations.
- **Valid Range:** `0.0` to `1000.0` nmol/L.

Any physiological values falling outside these veterinary thresholds trigger a validation exception and are rejected.

---

## 3. Darwin Core (DwC) Standard Mapping
All ingestible events are mapped to the international Darwin Core (DwC) standard utilizing the auxiliary `MeasurementOrFact` class to facilitate open-science sharing and indexing.

| Darwin Core Property | EthoPipe Model Mapping | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `dwc:individualID` | `subject_id` / `animal_id` | `canine-42` | Subject Identifier |
| `dwc:eventDate` | `timestamp` | `2026-06-30T19:57:00Z` | Event timestamp (ISO 8601) |
| `dwc:measurementType` | `measurementType` | `heart_rate_bpm` / `play_bow` | Behavior or vital sign |
| `dwc:measurementValue` | `measurementValue` | `88` | Measured value |
| `dwc:measurementUnit` | `measurementUnit` | `bpm` / `nmol/L` | Metric unit |
| `dwc:basisOfRecord` | `basisOfRecord` | `HumanObservation` / `MachineObservation` | Methodology |

---

## 4. Linguistic De-biasing and Anthropomorphic Filtering
To maintain scientific objectivity, any subjective terms descriptive of an animal's emotional state, intentionality, or human-projection traits must be filtered out or rejected.
- **Prohibited Subjective Words:** `stubborn`, `angry`, `spiteful`, `vicious`, `mean`, `happy`, `sad`, `frustrated`, `guilty`.
- **Preferred Objective Terms:** Focus purely on physical motor postures and observable sequences (e.g., `sphinx posture`, `tail carriage low`, `lip licking`, `ears pinned`, `vocalizing`).
