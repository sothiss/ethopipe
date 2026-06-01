import json
import pytest
from fastapi.testclient import TestClient

from ethopipe.api import app, get_loader
from ethopipe.loader import BaseLoader
from ethopipe.models import EthologicalObservation, QuarantineRecord


class MockLoader(BaseLoader):
    """Clean mock implementation of BaseLoader for decoupled API testing."""

    async def load_observation(self, observation: EthologicalObservation) -> str:
        return "mock-doc-single-id"

    async def load_observations_batch(self, observations: list[EthologicalObservation]) -> list[str]:
        return [f"mock-doc-batch-id-{i}" for i in range(len(observations))]

    async def load_quarantine_batch(self, quarantine_records: list[QuarantineRecord]) -> list[str]:
        return [f"mock-quarantine-batch-id-{i}" for i in range(len(quarantine_records))]


@pytest.fixture
def client() -> TestClient:
    """Fixture supplying a configured TestClient with mocked persistence dependencies."""
    app.dependency_overrides[get_loader] = lambda: MockLoader()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def get_api_test_payload() -> dict:
    """Helper to return a valid raw payload for testing."""
    return {
        "DogID": "SUB-DOG-500",
        "LocalTime": "2026-05-27T10:00:00",
        "Locality": "Facility Room 1",
        "Behavior": "Growling",
        "Value": "3 events",
        "Rating": 3,
        "HeartRateBPM": 85,
        "RecordBasis": "HumanObservation",
        "Notes": "Growled during visual stimulus.",
        "DogSizeCategory": "Small"
    }


def test_validate_endpoint_success(client):
    """Verify that /validate statelessly validates a raw payload and normalizes it."""
    payload = get_api_test_payload()
    mapping = {
        "DogID": "subject_id",
        "LocalTime": "timestamp",
        "Locality": "location",
        "Behavior": "behavior_type",
        "Value": "behavior_value",
        "Rating": "severity_score",
        "HeartRateBPM": "heart_rate",
        "RecordBasis": "observation_method",
        "Notes": "narrative",
        "DogSizeCategory": "dog_size_category"
    }
    response = client.post(f"/validate?mapping={json.dumps(mapping)}", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert Title Case was normalized to snake_case
    assert data["behavior_type"] == "growling"
    # Assert ontology URI was auto-resolved
    assert data["behavior_type_id"] == "http://purl.obolibrary.org/obo/GO_0071625"
    assert data["subject_id"] == "SUB-DOG-500"
    assert data["location"] == "Facility Room 1"


def test_validate_endpoint_failure(client):
    """Verify that /validate rejects invalid data with 422 Unprocessable Entity."""
    payload = get_api_test_payload()
    # Invalid heart rate (above max limit of 180 for Small dogs)
    payload["HeartRateBPM"] = 190
    
    mapping = {
        "DogID": "subject_id",
        "LocalTime": "timestamp",
        "Locality": "location",
        "Behavior": "behavior_type",
        "Value": "behavior_value",
        "Rating": "severity_score",
        "HeartRateBPM": "heart_rate",
        "RecordBasis": "observation_method",
        "Notes": "narrative",
        "DogSizeCategory": "dog_size_category"
    }
    response = client.post(f"/validate?mapping={json.dumps(mapping)}", json=payload)
    assert response.status_code == 422
    
    errors = response.json()["detail"]["errors"]
    assert any("out of veterinary bounds" in err for err in errors)


def test_validate_endpoint_bad_json(client):
    """Verify that /validate returns 400 Bad Request for unparseable payloads."""
    response = client.post("/validate", content="{invalid-json}")
    assert response.status_code == 400
    assert "payload must be a valid json object" in response.json()["detail"].lower()


def test_ingest_csv_endpoint(client):
    """Verify CSV batch ingestion, normalization, and quarantine handling."""
    csv_payload = (
        "DogID,LocalTime,Locality,Behavior,Value,Rating,HeartRateBPM,RecordBasis,Notes,DogSizeCategory\n"
        "SUB-DOG-501,2026-05-27T10:00:00,Yard,Whining,5,2,95,HumanObservation,Whined at gate,Small\n"
        "SUB-DOG-502,2026-05-27T10:00:00,Yard,invalid_behavior,5,2,95,HumanObservation,Bad row,Small\n"
        "SUB-DOG-503,2026-05-27T10:00:00,Yard,Panting,1,1,195,HumanObservation,High HR,Small\n"
    )

    mapping = {
        "DogID": "subject_id",
        "LocalTime": "timestamp",
        "Locality": "location",
        "Behavior": "behavior_type",
        "Value": "behavior_value",
        "Rating": "severity_score",
        "HeartRateBPM": "heart_rate",
        "RecordBasis": "observation_method",
        "Notes": "narrative",
        "DogSizeCategory": "dog_size_category"
    }

    # Pass mapping as query string
    response = client.post(
        f"/ingest/csv?mapping={json.dumps(mapping)}",
        content=csv_payload,
        headers={"Content-Type": "text/plain"}
    )

    assert response.status_code == 200
    res_data = response.json()

    assert res_data["status"] == "partial_success"
    assert res_data["processed_count"] == 3
    assert res_data["valid_count"] == 1
    assert res_data["quarantine_count"] == 2

    # Row 1 is valid (Whining)
    assert len(res_data["loaded_ids"]) == 1
    assert "mock-doc-batch-id-0" in res_data["loaded_ids"]

    # Quarantine ids should be populated
    assert len(res_data["quarantine_ids"]) == 2
    assert "mock-quarantine-batch-id-0" in res_data["quarantine_ids"]

    # Row 2 is quarantined (invalid_behavior)
    assert "2" in res_data["quarantine"]
    assert any("behavior_type" in err for err in res_data["quarantine"]["2"])

    # Row 3 is quarantined (HR 195 is out of bounds for Small dog)
    assert "3" in res_data["quarantine"]
    assert any("out of veterinary bounds" in err for err in res_data["quarantine"]["3"])


def test_ingest_json_endpoint(client):
    """Verify JSON list batch ingestion, normalization, and quarantine handling."""
    json_payload = [
        {
            "DogID": "SUB-DOG-601",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "Yawning",
            "Value": "2 yawning events",
            "Rating": 1,
            "HeartRateBPM": 80,
            "RecordBasis": "HumanObservation",
            "Notes": "Standard yawning.",
            "DogSizeCategory": "Medium"
        },
        {
            "DogID": "SUB-DOG-602",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "Avoidance",
            "Value": "1 event",
            "Rating": 2,
            "HeartRateBPM": 40,  # Below min HR (50) for Medium dogs
            "RecordBasis": "HumanObservation",
            "Notes": "Low HR.",
            "DogSizeCategory": "Medium"
        }
    ]

    mapping = {
        "DogID": "subject_id",
        "LocalTime": "timestamp",
        "Locality": "location",
        "Behavior": "behavior_type",
        "Value": "behavior_value",
        "Rating": "severity_score",
        "HeartRateBPM": "heart_rate",
        "RecordBasis": "observation_method",
        "Notes": "narrative",
        "DogSizeCategory": "dog_size_category"
    }

    response = client.post(
        f"/ingest/json?mapping={json.dumps(mapping)}",
        json=json_payload
    )

    assert response.status_code == 200
    res_data = response.json()

    assert res_data["status"] == "partial_success"
    assert res_data["processed_count"] == 2
    assert res_data["valid_count"] == 1
    assert res_data["quarantine_count"] == 1

    # Record 1 is valid (Yawning)
    assert len(res_data["loaded_ids"]) == 1
    assert "mock-doc-batch-id-0" in res_data["loaded_ids"]

    # Quarantine ids should be populated
    assert len(res_data["quarantine_ids"]) == 1
    assert "mock-quarantine-batch-id-0" in res_data["quarantine_ids"]

    # Record 2 is quarantined
    assert "2" in res_data["quarantine"]
    assert any("out of veterinary bounds" in err for err in res_data["quarantine"]["2"])
