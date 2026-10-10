from unittest.mock import patch

import pytest
import sentry_sdk
from fastapi.testclient import TestClient

from src.pipeline.agent import run_ethopipe_agent
from src.pipeline.api import app

client = TestClient(app)


def get_valid_payload() -> dict:
    return {
        "ObservationID": "obs-agent-01",
        "SubjectID": "dog-123",
        "Timestamp_ISO8601": "2026-07-05T12:00:00Z",
        "Location": "Lab A",
        "Context/Session": "Play session with familiar dog.",
        "behaviors": [
            {
                "Behavior": "PlayBow",
                "Behav_Intensity": "High",
                "Additional_Notes": "Relaxed posture.",
            }
        ],
        "physiology": {
            "HeartRate_BPM": 95,
            "RespRate_BPM": 22,
            "BodyTemp_C": 38.7,
            "Cortisol_nmolL": 180.0,
        },
    }


def test_sentry_sdk_initialized():
    """Verify Sentry SDK has active client with required Agent Tracing options."""
    sentry_client = sentry_sdk.get_client()
    assert sentry_client is not None
    assert sentry_client.is_active()
    options = sentry_client.options
    assert options.get("traces_sample_rate") == 1.0
    assert options.get("send_default_pii") is True
    assert "ingest.us.sentry.io" in options.get("dsn", "")


def test_run_ethopipe_agent_spans_and_conversations():
    """Verify agent creates spans and sets conversation ID."""
    with (
        patch("sentry_sdk.ai.set_conversation_id") as mock_set_conv,
        patch("sentry_sdk.set_user") as mock_set_user,
    ):
        payload = get_valid_payload()

        result = run_ethopipe_agent(
            prompt="Process observation obs-agent-01",
            incident_data=payload,
            conversation_id="conv_session_789",
            user_id="researcher_alice",
        )

        assert result["status"] == "success"
        assert result["conversation_id"] == "conv_session_789"
        assert result["incident"]["ObservationID"] == "obs-agent-01"
        assert "Observation processed successfully" in result["response"]

        mock_set_conv.assert_called_once_with("conv_session_789")
        mock_set_user.assert_called_once_with(
            {"id": "researcher_alice", "username": "researcher_alice"}
        )


def test_agent_run_endpoint_unauthenticated():
    response = client.post("/agent/run", json={"prompt": "Hello"})
    assert response.status_code == 401


def test_agent_run_endpoint_authenticated(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")

    req_body = {
        "prompt": "Evaluate canine play posture",
        "conversation_id": "conv_abc_123",
        "incident_data": get_valid_payload(),
    }

    response = client.post(
        "/agent/run",
        json=req_body,
        auth=("admin", "secret"),
        headers={"X-Conversation-ID": "conv_abc_123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["conversation_id"] == "conv_abc_123"
    assert data["incident"]["ObservationID"] == "obs-agent-01"


def test_debug_sentry_endpoint(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")

    # The debug-sentry endpoint deliberately raises RuntimeError to verify capture
    with pytest.raises(RuntimeError, match="Deliberate Sentry test error"):
        client.get(
            "/debug-sentry?message=pytest-verification",
            auth=("admin", "secret"),
        )
