from datetime import datetime, timedelta
from typing import cast
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.pipeline.models import (
    BehaviorObservation,
    BehaviorType,
    CanineObservation,
    EthologicalIncident,
    PhysioMeasurement,
)
from src.pipeline.parser import normalize_incident


def test_valid_incident_legacy() -> None:
    incident = EthologicalIncident(
        animal_id=uuid4(),
        heart_rate=80,
        behavior_type="neutral",
        handler_notes="Calm baseline observation.",
    )
    assert incident.heart_rate == 80
    assert incident.behavior_type == "neutral"


def test_legacy_incident_subjective_rejected() -> None:
    with pytest.raises(ValidationError):
        EthologicalIncident(
            animal_id=uuid4(),
            heart_rate=80,
            behavior_type="neutral",
            handler_notes="A stubborn and angry dog.",
        )


def test_valid_canine_observation() -> None:
    obs = CanineObservation(
        observation_id="obs-001",
        subject_id="dog-123",
        timestamp=datetime.now(),
        location="Lab A",
        behaviors=[
            BehaviorObservation(
                behavior=BehaviorType.PLAY_BOW,
                intensity="High",
                additional_notes="Subject plays; body posture low.",
            )
        ],
        physiology=PhysioMeasurement(
            heart_rate_bpm=100,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        ),
    )
    assert obs.observation_id == "obs-001"
    assert obs.subject_id == "dog-123"
    assert obs.behaviors[0].behavior == BehaviorType.PLAY_BOW
    assert obs.physiology.heart_rate_bpm == 100


def test_canine_observation_strict_mode() -> None:
    # Under strict=True, passing strings for numeric values should fail
    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=cast(int, "100"),  # String instead of int
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        )


def test_physiological_clamping() -> None:
    # Heart rate out of bounds (<30 or >250)
    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=20,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        )

    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=260,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        )

    # Respiration out of bounds (<0 or >200)
    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=100,
            resp_rate_bpm=210,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        )

    # Temperature out of bounds (<36.0 or >41.0)
    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=100,
            resp_rate_bpm=20,
            body_temp_c=35.9,
            cortisol_nmolL=150.0,
        )


def test_size_dependent_heart_rate() -> None:
    # Toy breeds: 80 - 200 BPM
    # Valid Toy
    obs_toy_valid = CanineObservation(
        observation_id="obs-001",
        subject_id="dog-123",
        timestamp=datetime.now(),
        dog_size="Toy",
        behaviors=[BehaviorObservation(behavior=BehaviorType.SIT)],
        physiology=PhysioMeasurement(
            heart_rate_bpm=150,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        ),
    )
    assert obs_toy_valid.physiology.heart_rate_bpm == 150

    # Invalid Toy (too low)
    with pytest.raises(ValidationError):
        CanineObservation(
            observation_id="obs-001",
            subject_id="dog-123",
            timestamp=datetime.now(),
            dog_size="Toy",
            behaviors=[BehaviorObservation(behavior=BehaviorType.SIT)],
            physiology=PhysioMeasurement(
                heart_rate_bpm=75,
                resp_rate_bpm=20,
                body_temp_c=38.5,
                cortisol_nmolL=150.0,
            ),
        )

    # Giant breeds: 40 - 110 BPM
    # Valid Giant
    obs_giant_valid = CanineObservation(
        observation_id="obs-001",
        subject_id="dog-123",
        timestamp=datetime.now(),
        dog_size="Giant",
        behaviors=[BehaviorObservation(behavior=BehaviorType.SIT)],
        physiology=PhysioMeasurement(
            heart_rate_bpm=60,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        ),
    )
    assert obs_giant_valid.physiology.heart_rate_bpm == 60

    # Invalid Giant (too high)
    with pytest.raises(ValidationError):
        CanineObservation(
            observation_id="obs-001",
            subject_id="dog-123",
            timestamp=datetime.now(),
            dog_size="Giant",
            behaviors=[BehaviorObservation(behavior=BehaviorType.SIT)],
            physiology=PhysioMeasurement(
                heart_rate_bpm=120,
                resp_rate_bpm=20,
                body_temp_c=38.5,
                cortisol_nmolL=150.0,
            ),
        )


def test_behavior_duration_validation() -> None:
    now = datetime.now()
    # end_time >= start_time is valid
    BehaviorObservation(
        behavior=BehaviorType.SIT, start_time=now, end_time=now + timedelta(seconds=10)
    )

    # end_time < start_time is invalid
    with pytest.raises(ValidationError):
        BehaviorObservation(
            behavior=BehaviorType.SIT,
            start_time=now,
            end_time=now - timedelta(seconds=10),
        )


def test_subjective_notes_rejection() -> None:
    # Subjective terms like 'angry', 'stubborn', 'spiteful' must raise validation error
    with pytest.raises(ValidationError):
        BehaviorObservation(
            behavior=BehaviorType.BARK,
            additional_notes="The subject is very angry and stubborn.",
        )


def test_parser_de_biasing_deletion() -> None:
    # Parser must actively strip prohibited subjective terms
    payload = {
        "ObservationID": "obs-001",
        "SubjectID": "dog-123",
        "Timestamp_ISO8601": datetime.now().isoformat(),
        "behaviors": [
            {
                "Behavior": "Sit",
                "Additional_Notes": (
                    "The dog was stubborn but eventually sat. He seemed angry."
                ),
            }
        ],
        "physiology": {
            "HeartRate_BPM": 80,
            "RespRate_BPM": 20,
            "BodyTemp_C": 38.5,
            "Cortisol_nmolL": 100.0,
        },
    }
    obs = normalize_incident(payload)
    # Prohibited words 'stubborn' and 'angry' must be deleted
    notes = obs.behaviors[0].additional_notes
    assert notes is not None
    assert "stubborn" not in notes.lower()
    assert "angry" not in notes.lower()
    assert notes == "The dog was but eventually sat. He seemed ."


def test_darwin_core_mapping() -> None:
    obs = CanineObservation(
        observation_id="obs-001",
        subject_id="dog-123",
        timestamp=datetime(2026, 7, 5, 12, 0, 0),
        behaviors=[
            BehaviorObservation(
                behavior=BehaviorType.PLAY_BOW,
                intensity="High",
            )
        ],
        physiology=PhysioMeasurement(
            heart_rate_bpm=95,
            resp_rate_bpm=22,
            body_temp_c=38.7,
            cortisol_nmolL=180.0,
        ),
    )
    dwc_records = obs.to_dwc()
    assert len(dwc_records) == 5

    # Check serialization format
    serialized = [r.model_dump(by_alias=True) for r in dwc_records]

    # Verify keys contain colons
    for s in serialized:
        assert "dwc:individualID" in s
        assert "dwc:eventDate" in s
        assert "dwc:measurementType" in s
        assert "dwc:measurementValue" in s
        assert "dwc:basisOfRecord" in s

    # Verify values
    assert serialized[0]["dwc:measurementType"] == "Play Bow"
    assert serialized[0]["dwc:measurementValue"] == "High"
    assert serialized[0]["dwc:basisOfRecord"] == "HumanObservation"

    assert serialized[1]["dwc:measurementType"] == "heart_rate_bpm"
    assert serialized[1]["dwc:measurementValue"] == "95"
    assert serialized[1]["dwc:basisOfRecord"] == "MachineObservation"
