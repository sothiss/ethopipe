from fastapi.testclient import TestClient

from src.pipeline.api import app

client = TestClient(app)


def get_valid_observation_payload() -> dict:
    return {
        "ObservationID": "obs-001",
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


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "EthoPipe API is running"}


def test_ingest_incident_unauthenticated():
    payload = get_valid_observation_payload()
    response = client.post("/ingest", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_ingest_incident_incorrect_credentials(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    payload = get_valid_observation_payload()
    response = client.post(
        "/ingest", json=payload, auth=("wronguser", "wrongpassword")
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_ingest_incident_authenticated(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    payload = get_valid_observation_payload()
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 200
    assert response.json()["status"] == "valid"
    assert response.json()["incident"]["ObservationID"] == payload["ObservationID"]
    assert (
        response.json()["incident"]["physiology"]["HeartRate_BPM"]
        == payload["physiology"]["HeartRate_BPM"]
    )


def test_ingest_incident_unconfigured_credentials(monkeypatch):
    monkeypatch.delenv("API_USERNAME", raising=False)
    monkeypatch.delenv("API_PASSWORD", raising=False)
    payload = get_valid_observation_payload()
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal Server Error",
    }


def test_ingest_invalid_heart_rate(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    payload = get_valid_observation_payload()
    payload["physiology"]["HeartRate_BPM"] = 280  # Exceeds max 250
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 422


def test_ingest_subjective_notes_rejected(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    payload = get_valid_observation_payload()
    payload["behaviors"][0]["Additional_Notes"] = (
        "The dog was very stubborn."  # Prohibited word
    )
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 422
    assert "stubborn" in response.text
