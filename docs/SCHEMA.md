# EthoPipe Schema Specification

This document details the data schemas and structures used in the EthoPipe ethological data ingestion pipeline. To maintain mathematical and biological determinism, all models are built using **Pydantic v2** with strict type enforcement (`model_config = ConfigDict(strict=True)`).

---

## 1. CanineObservation Schema (Core Observation Payload)

The primary data payload representing an observed canine ethological event, capturing behavioral motor patterns and physiological telemetry.

### Properties and Fields

| Field Name | Type | Constraints / Validation | Description |
| :--- | :--- | :--- | :--- |
| `observation_id` | `str` | Max length: 64 chars | Unique tracking identifier for the observation event. |
| `subject_id` | `str` | Max length: 64 chars | Identifier for the canine subject (maps to `dwc:individualID`). |
| `timestamp` | `datetime` | UTC timestamp | Incident date/time (maps to `dwc:eventDate` ISO 8601). |
| `behaviors` | `list[BehaviorObservation]` | Non-empty list | Observed behavioral syllables (motor patterns). |
| `physiology` | `PhysioMeasurement \| None` | Validated physio block | Real-time vital signs telemetry. |
| `size_category` | `Literal["Toy", "Giant", "Standard"] \| None` | Bounded enum | Morphological size category for HR bounds. |

---

## 2. PhysioMeasurement Schema (Vital Telemetry)

Enforces physiological thresholds anchored in peer-reviewed veterinary literature (e.g. *Merck Veterinary Manual*):

| Field Name | Type | Valid Range | Unit / Description |
| :--- | :--- | :--- | :--- |
| `heart_rate_bpm` | `int` | `30` to `250` BPM | Heart rate in beats per minute. Clamped by size category when known. |
| `resp_rate_bpm` | `int` | `10` to `120` BPM | Respiration rate in breaths per minute. |
| `body_temp_c` | `float` | `36.0` to `41.5` °C | Core body temperature in degrees Celsius. |
| `cortisol_nmolL` | `float \| None` | `0.0` to `1000.0` | Serum or salivary cortisol biomarker concentration. |

---

## 3. BehaviorObservation Schema (Motor Syllables)

Standardizes motor ethograms and strips subjective human bias:

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `behavior` | `BehaviorType` | Enum / O(1) lookup | Standard syllable (e.g. `PlayBow`, `Sit`, `Barks`, `Panting`). |
| `intensity` | `str \| None` | `Low \| Moderate \| High \| NA` | Objective categorical intensity. |
| `start_time` | `datetime \| None` | ISO 8601 | Start timestamp of behavioral syllable. |
| `end_time` | `datetime \| None` | Must be `>= start_time` | End timestamp of behavioral syllable. |
| `additional_notes` | `str \| None` | De-biased text | Notes stripped of subjective/anthropomorphic terms. |

---

## 4. Darwin Core (`MeasurementOrFact`) Schema

Direct mapping onto international biodiversity informatics standards (GBIF / OBIS):

```json
{
  "title": "MeasurementOrFact",
  "type": "object",
  "properties": {
    "dwc:individualID": { "type": "string", "description": "Canine subject identifier" },
    "dwc:eventDate": { "type": "string", "format": "date-time" },
    "dwc:measurementType": { "type": "string", "description": "e.g. heart_rate_bpm or play_bow" },
    "dwc:measurementValue": { "type": ["string", "number"] },
    "dwc:measurementUnit": { "type": "string", "description": "e.g. bpm, nmol/L, or syllable" },
    "dwc:basisOfRecord": { "type": "string", "enum": ["HumanObservation", "MachineObservation"] }
  },
  "required": ["dwc:individualID", "dwc:eventDate", "dwc:measurementType", "dwc:measurementValue"]
}
```

---

## 5. Legacy EthologicalIncident Schema (Backward Compatibility)

Maintained for existing REST API endpoints:
- `animal_id`: UUID
- `timestamp`: UTC datetime
- `heart_rate`: Integer bounded between 30 and 250 BPM
- `behavior_type`: Categorical ethogram state
- `handler_notes`: Text with anthropomorphic word filtering
