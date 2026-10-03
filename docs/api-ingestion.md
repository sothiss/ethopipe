---
description: Submit validated canine observations to the EthoPipe API.
---

# API ingestion

## API ingestion

The API accepts validated canine observations at `POST /ingest`.

Configure HTTP Basic credentials on the server before sending requests:

* `API_USERNAME`
* `API_PASSWORD`

The endpoint returns `401` for missing or invalid credentials. It returns `500` if server credentials are not configured.

### Submit an observation

Send `Content-Type: application/json` with HTTP Basic authentication.

```json
{
  "ObservationID": "obs-001",
  "SubjectID": "dog-123",
  "Timestamp_ISO8601": "2026-07-05T12:00:00Z",
  "Location": "Lab A",
  "Context/Session": "Play session with familiar dog.",
  "behaviors": [
    {
      "Behavior": "PlayBow",
      "Behav_Intensity": "High",
      "Additional_Notes": "Low front posture; forelimbs extended."
    }
  ],
  "physiology": {
    "HeartRate_BPM": 95,
    "RespRate_BPM": 22,
    "BodyTemp_C": 38.7,
    "Cortisol_nmolL": 180.0
  }
}
```

A valid request returns `200` and echoes the accepted observation:

```json
{
  "status": "valid",
  "incident": {}
}
```

### Validation requirements

Use JSON numbers for physiological values. String values are rejected.

| Field               | Requirement                        |
| ------------------- | ---------------------------------- |
| `ObservationID`     | Observation identifier.            |
| `SubjectID`         | Subject identifier.                |
| `Timestamp_ISO8601` | ISO 8601 timestamp.                |
| `behaviors`         | At least one behavior observation. |
| `HeartRate_BPM`     | Integer from `30` through `250`.   |
| `RespRate_BPM`      | Integer from `0` through `200`.    |
| `BodyTemp_C`        | Number from `36.0` through `41.0`. |
| `Cortisol_nmolL`    | Number from `0.0` through `600.0`. |

When `DogSize` is present, heart-rate limits narrow further:

* `Toy`: `80` through `200` BPM.
* `Giant`: `40` through `110` BPM.

Use observable behavior descriptions in free-text fields. The API rejects these terms: `stubborn`, `angry`, `spiteful`, `vicious`, `mean`, `happy`, `sad`, `frustrated`, and `guilty`.

### Response errors

| Status | Meaning                                        |
| ------ | ---------------------------------------------- |
| `200`  | The observation passed validation.             |
| `401`  | Authentication is missing or invalid.          |
| `422`  | The payload failed validation.                 |
| `500`  | Server authentication credentials are missing. |

See the [VALIDATION.md](VALIDATION.md "mention") for the complete constraints.
