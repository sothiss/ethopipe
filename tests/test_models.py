from uuid import uuid4

from src.pipeline.models import EthologicalIncident


def test_valid_incident() -> None:
    incident = EthologicalIncident(
        animal_id=uuid4(),
        heart_rate=80,
        behavior_type="neutral",
        handler_notes="Calm baseline observation.",
    )

    assert incident.heart_rate == 80
    assert incident.behavior_type == "neutral"
