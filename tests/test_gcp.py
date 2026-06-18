import json
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
import httpx
from fastapi.testclient import TestClient

from ethopipe.api import app
from ethopipe.models import EthologicalObservation
from ethopipe.gcp import (
    download_gcs_file,
    _to_vertex_schema,
    call_vertex_ai_for_extraction,
    process_narrative_with_gcp,
)


from ethopipe.api import get_loader
from ethopipe.loader import BaseLoader


class MockLoader(BaseLoader):
    async def load_observation(self, observation) -> str:
        return "mock-doc-single-id"

    async def load_observations_batch(self, observations) -> list[str]:
        return [f"mock-doc-batch-id-{i}" for i in range(len(observations))]

    async def load_quarantine_batch(self, quarantine_records) -> list[str]:
        return [f"mock-quarantine-batch-id-{i}" for i in range(len(quarantine_records))]


@pytest.fixture
def client():
    app.dependency_overrides[get_loader] = lambda: MockLoader()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_to_vertex_schema():
    """Verify conversion of standard JSON schema to Vertex AI uppercase schema."""
    input_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "count": {"type": "integer"},
            "items": {
                "type": "array",
                "items": {"type": "object", "properties": {"id": {"type": "string"}}}
            }
        },
        "required": ["name"]
    }
    expected = {
        "type": "OBJECT",
        "properties": {
            "name": {"type": "STRING"},
            "count": {"type": "INTEGER"},
            "items": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {"id": {"type": "STRING"}}
                }
            }
        },
        "required": ["name"]
    }
    assert _to_vertex_schema(input_schema) == expected


@patch("google.cloud.storage.Client")
def test_download_gcs_file(mock_storage_client):
    """Verify that download_gcs_file reads content from mocked storage bucket."""
    mock_client_inst = MagicMock()
    mock_storage_client.return_value = mock_client_inst
    
    mock_bucket = MagicMock()
    mock_client_inst.bucket.return_value = mock_bucket
    
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_blob.download_as_text.return_value = "Mock GCS file content"

    content = download_gcs_file("test-bucket", "subdir/dog1.txt")
    
    assert content == "Mock GCS file content"
    mock_storage_client.assert_called_once()
    mock_client_inst.bucket.assert_called_once_with("test-bucket")
    mock_bucket.blob.assert_called_once_with("subdir/dog1.txt")
    mock_blob.download_as_text.assert_called_once_with(encoding="utf-8")


@pytest.mark.anyio
@patch("google.auth.default")
@patch("httpx.AsyncClient.post")
async def test_call_vertex_ai_for_extraction(mock_post, mock_auth_default):
    """Verify calling Vertex AI API endpoint and successfully parsing extraction response."""
    # Mock GCP Auth
    mock_creds = MagicMock()
    mock_creds.token = "mock-token"
    mock_auth_default.return_value = (mock_creds, "mock-project-id")

    # Mock HTTP response from Vertex AI
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    
    # Standard response payload structure returned by Gemini in Vertex AI
    vertex_ai_response = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps({
                                "observations": [
                                    {
                                        "behavior": "lip_licking",
                                        "ontology_uri": "NBO:0000216",
                                        "source_text": "lip licking twice",
                                        "confidence_score": 0.95
                                    },
                                    {
                                        "behavior": "tail_tuck",
                                        "ontology_uri": "VT:0000030",
                                        "source_text": "tail tucked",
                                        "confidence_score": 0.85
                                    }
                                ]
                            })
                        }
                    ]
                }
            }
        ]
    }
    mock_response.json.return_value = vertex_ai_response
    mock_post.return_value = mock_response

    log = await call_vertex_ai_for_extraction(
        narrative="Subject was seen trembling and lip licking twice with tail tucked.",
        project_id="test-proj",
        location="us-central1"
    )

    assert len(log.observations) == 2
    assert log.observations[0].behavior == "lip_licking"
    assert log.observations[0].confidence_score == 0.95
    assert log.observations[1].behavior == "tail_tuck"
    assert log.observations[1].confidence_score == 0.85

    mock_post.assert_called_once()
    # Check headers
    args, kwargs = mock_post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer mock-token"
    assert "generationConfig" in kwargs["json"]


@pytest.mark.anyio
@patch("google.auth.default")
@patch("httpx.AsyncClient.post")
async def test_call_vertex_ai_failures(mock_post, mock_auth_default):
    """Verify that call_vertex_ai raises exception on non-200 response."""
    mock_creds = MagicMock()
    mock_creds.token = "mock-token"
    mock_auth_default.return_value = (mock_creds, "mock-project-id")

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    with pytest.raises(httpx.HTTPStatusError):
        await call_vertex_ai_for_extraction("test text")


@pytest.mark.anyio
@patch("ethopipe.gcp.call_vertex_ai_for_extraction")
async def test_process_narrative_with_gcp(mock_vertex_call):
    """Verify the hybrid extraction pipeline extracting vitals via regex and behaviors via Vertex."""
    from ethopipe.models import EthogramExtractionLog, BehavioralObservation

    # Mock Vertex AI behavior extraction output
    mock_vertex_call.return_value = EthogramExtractionLog(
        observations=[
            BehavioralObservation(
                behavior="lip_licking",
                ontology_uri="http://purl.obolibrary.org/obo/NBO_0000216",
                source_text="licking lips twice",
                confidence_score=0.9
            ),
            BehavioralObservation(
                behavior="trembling",
                ontology_uri="http://purl.obolibrary.org/obo/NBO_0000589",
                source_text="trembling continuously",
                confidence_score=0.95
            )
        ]
    )

    narrative = "Subject had a heart rate of 90 bpm, temp of 38.5 C, trembling continuously and licking lips twice. Saliva cortisol level was 3.5 ng/mL."
    timestamp = datetime.now()

    observations = await process_narrative_with_gcp(
        narrative=narrative,
        subject_id="SUB-DOG-99",
        timestamp=timestamp,
        location="Lab A",
        dog_size_category="Medium"
    )

    assert len(observations) == 2
    
    # Both observations must inherit parsed vitals
    for obs in observations:
        assert obs.subject_id == "SUB-DOG-99"
        assert obs.heart_rate == 90
        assert obs.body_temp == 38.5
        assert obs.cortisol_level == 3.5
        assert obs.cortisol_matrix == "saliva"
        assert obs.location == "Lab A"

    # Behavior specific values
    assert observations[0].behavior_type == "lip_licking"
    assert observations[0].behavior_value == 2  # Resolved from "twice"
    assert observations[0].behavior_type_id == "http://purl.obolibrary.org/obo/NBO_0000216"

    assert observations[1].behavior_type == "trembling"
    assert observations[1].behavior_value == "continuous"  # Resolved from "continuously"
    assert observations[1].behavior_type_id == "http://purl.obolibrary.org/obo/NBO_0000589"


@pytest.mark.anyio
@patch("ethopipe.gcp.call_vertex_ai_for_extraction")
async def test_process_narrative_with_gcp_fallback_regex(mock_vertex_call):
    """Verify that process_narrative_with_gcp falls back to regex parser if Vertex fails."""
    mock_vertex_call.side_effect = RuntimeError("Vertex API Error")

    narrative = "Subject displayed lunges twice. Heart rate 80 bpm."
    timestamp = datetime.now()

    observations = await process_narrative_with_gcp(
        narrative=narrative,
        subject_id="SUB-DOG-99",
        timestamp=timestamp,
        location="Lab A",
        dog_size_category="Medium"
    )

    # Fallback to local regex-based parsing should catch "lunges"
    assert len(observations) == 1
    assert observations[0].behavior_type == "lunges"
    assert observations[0].behavior_value == 2
    assert observations[0].heart_rate == 80


@patch("ethopipe.gcp.download_gcs_file")
@patch("ethopipe.gcp.process_narrative_with_gcp")
def test_gcp_trigger_api_endpoint(mock_process, mock_download, client):
    """Verify that POST /gcp/trigger route receives event payload and executes pipeline."""
    mock_loader = AsyncMock()
    mock_loader.load_observations_batch.return_value = ["mock-doc-id-1"]
    app.dependency_overrides[get_loader] = lambda: mock_loader

    mock_download.return_value = "Raw notes: trembling observed, hr is 75"
    
    mock_obs = EthologicalObservation(
        subject_id="SUB-DOG-88",
        timestamp=datetime.now(),
        location="Room A",
        behavior_type="trembling",
        behavior_value=1,
        heart_rate=75,
        observation_method="HumanObservation",
        narrative="Raw notes: trembling observed, hr is 75"
    )
    mock_process.return_value = [mock_obs]

    # Eventarc storage object finalized envelope
    payload = {
        "data": {
            "bucket": "my-science-bucket",
            "name": "study-1/SUB-DOG-88_handler_notes.txt"
        },
        "location": "Evaluation Yard",
        "dog_size_category": "Large"
    }

    response = client.post("/gcp/trigger", json=payload)
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "success"
    assert res_data["bucket"] == "my-science-bucket"
    assert res_data["blob"] == "study-1/SUB-DOG-88_handler_notes.txt"
    assert res_data["extracted_count"] == 1
    assert res_data["loaded_ids"] == ["mock-doc-id-1"]

    mock_download.assert_called_once_with("my-science-bucket", "study-1/SUB-DOG-88_handler_notes.txt")
    mock_process.assert_called_once()
    
    # Verify auto-extracting subject_id from filename in endpoint
    args, kwargs = mock_process.call_args
    assert kwargs["subject_id"] == "SUB-DOG-88"
    assert kwargs["location"] == "Evaluation Yard"
    assert kwargs["dog_size_category"] == "Large"
