# EthoPipe Validation Specification

This document details the validation constraints and mappings enforced by the EthoPipe data pipeline. All observational inputs must satisfy these criteria to be accepted into the data store.

## 1. Schema Validation (Pydantic v2)
Every ingestion endpoint enforces Pydantic v2 schemas executing under strict mode configurations:
```python
model_config = ConfigDict(strict=True)
```
Any type coercion (e.g., parsing a string `"80"` into an integer `80` or accepting malformed UUID strings) is rejected at the entry point to preserve datatype precision.

## 2. Veterinary Physiological Clamping
To prevent corrupted entries or data contamination, physiological metrics must comply with peer-reviewed veterinary benchmarks. 

### Canine Heart Rate Constraints
The absolute boundaries for canine heart rates are clamped strictly:
- **Absolute Minimum:** `30` BPM
- **Absolute Maximum:** `250` BPM

Additionally, if size classification metadata is present, the following size-dependent parameters apply:
- **Toy Breeds (e.g., Chihuahua, Pomeranian):** Bounded strictly between `80` and `200` BPM.
- **Giant Breeds (e.g., Great Dane, Mastiff):** Bounded strictly between `40` and `110` BPM.

Any heart rate values falling outside these thresholds must raise a validation exception and be discarded.

## 3. Darwin Core (DwC) Standard Mapping
All ingestible events are mapped to the international Darwin Core (DwC) standard utilizing the auxiliary `MeasurementOrFact` class to facilitate open-science sharing and indexing.

| Darwin Core Property | EthoPipe Model Mapping | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `dwc:individualID` | `animal_id` | `859c2356-9a2c-...` | Subject ID |
| `dwc:eventDate` | `timestamp` | `2026-06-30T19:57:00Z` | Event timestamp (ISO 8601) |
| `dwc:measurementType` | `behavior_type` | `barks` | Motor behavior / symptom |
| `dwc:measurementValue` | `heart_rate` | `88` | Measured value of the behavior/physiological metric |
| `dwc:basisOfRecord` | Constant value | `HumanObservation` | Origin of the data record |

## 4. Linguistic De-biasing and Anthropomorphic Filtering
To maintain scientific objectivity, any subjective terms descriptive of an animal's emotional state, intentionality, or human-projection traits must be filtered out or rejected.
- **Prohibited Subjective Words:** `stubborn`, `angry`, `spiteful`, `vicious`, `mean`, `happy`, `sad`, `frustrated`, `guilty`.
- **Preferred Objective Terms:** Focus purely on physical motor postures and observable sequences (e.g., `sphinx posture`, `tail carriage low`, `lip licking`, `ears pinned`, `vocalizing`).
