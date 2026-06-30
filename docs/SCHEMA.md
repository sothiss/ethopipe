# EthoPipe Schema Specification

This document details the data schemas and structures used in the EthoPipe ethological data ingestion pipeline. To maintain mathematical and physical determinism, all models are built using **Pydantic v2** with strict type enforcement.

## EthologicalIncident Schema

The primary data payload representing an observed behavioral and physiological incident.

### Properties and Types

| Field Name | Data Type | Validation Rules / Constraints | Description |
| :--- | :--- | :--- | :--- |
| `animal_id` | `UUID` | Must be a valid UUID v4 | Unique identifier for the animal subject. |
| `timestamp` | `datetime` | Defaults to UTC `now` (ISO 8601) | Date and time the behavioral incident occurred. |
| `heart_rate` | `integer` | Strictly bounded: `gt=0`, `lt=300` | Measured vital heart rate. Subject to canine size-based clamping. |
| `behavior_type` | `string` | Regex pattern: `^(barks\|lunges\|cowers\|neutral\|vocalizing\|panting)$` | Categorical ethogram behavioral state classification. |
| `handler_notes` | `string` | Maximum length: `1000` characters | Textual descriptions. Must exclude subjective/anthropomorphic terms. |

### JSON Schema Definition

All incoming payloads are validated at the API boundary against this JSON schema structure:

```json
{
  "title": "EthologicalIncident",
  "type": "object",
  "properties": {
    "animal_id": {
      "title": "Animal Id",
      "type": "string",
      "format": "uuid"
    },
    "timestamp": {
      "title": "Timestamp",
      "type": "string",
      "format": "date-time"
    },
    "heart_rate": {
      "title": "Heart Rate",
      "type": "integer",
      "exclusiveMinimum": 0,
      "exclusiveMaximum": 300
    },
    "behavior_type": {
      "title": "Behavior Type",
      "type": "string",
      "pattern": "^(barks|lunges|cowers|neutral|vocalizing|panting)$"
    },
    "handler_notes": {
      "title": "Handler Notes",
      "type": "string",
      "maxLength": 1000
    }
  },
  "required": [
    "animal_id",
    "heart_rate",
    "behavior_type",
    "handler_notes"
  ]
}
```

### Ingestion Example Payload

```json
{
  "animal_id": "859c2356-9a2c-4672-88f5-667793d5df02",
  "timestamp": "2026-06-30T19:57:00Z",
  "heart_rate": 88,
  "behavior_type": "neutral",
  "handler_notes": "Subject sits in sphinx posture facing the handler; tail is relaxed."
}
```
