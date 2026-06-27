import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from src.pipeline.api import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "EthoPipe API is running"}

def test_ingest_incident_unauthenticated():
    incident_data = {
        "animal_id": str(uuid4()),
        "heart_rate": 80,
        "behavior_type": "neutral",
        "handler_notes": "Calm baseline observation."
    }
    response = client.post("/ingest", json=incident_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_ingest_incident_incorrect_credentials(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    incident_data = {
        "animal_id": str(uuid4()),
        "heart_rate": 80,
        "behavior_type": "neutral",
        "handler_notes": "Calm baseline observation."
    }
    response = client.post(
        "/ingest",
        json=incident_data,
        auth=("wronguser", "wrongpassword")
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_ingest_incident_authenticated(monkeypatch):
    monkeypatch.setenv("API_USERNAME", "admin")
    monkeypatch.setenv("API_PASSWORD", "secret")
    incident_data = {
        "animal_id": str(uuid4()),
        "heart_rate": 80,
        "behavior_type": "neutral",
        "handler_notes": "Calm baseline observation."
    }
    response = client.post(
        "/ingest",
        json=incident_data,
        auth=("admin", "secret")
    )
    assert response.status_code == 200
    assert response.json()["status"] == "valid"
    assert response.json()["incident"]["animal_id"] == incident_data["animal_id"]
    assert response.json()["incident"]["heart_rate"] == incident_data["heart_rate"]
    assert response.json()["incident"]["behavior_type"] == incident_data["behavior_type"]
    assert response.json()["incident"]["handler_notes"] == incident_data["handler_notes"]


def test_ingest_incident_unconfigured_credentials(monkeypatch):
    monkeypatch.delenv("API_USERNAME", raising=False)
    monkeypatch.delenv("API_PASSWORD", raising=False)
    incident_data = {
        "animal_id": str(uuid4()),
        "heart_rate": 80,
        "behavior_type": "neutral",
        "handler_notes": "Calm baseline observation."
    }
    response = client.post(
        "/ingest",
        json=incident_data,
        auth=("admin", "secret")
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Authentication credentials are not configured on the server"}
