from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EthologicalIncident(BaseModel):
    animal_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    heart_rate: int = Field(..., gt=0, lt=300)
    behavior_type: str = Field(
        ...,
        pattern=r"^(barks|lunges|cowers|neutral|vocalizing|panting)$",
    )
    handler_notes: str = Field(..., max_length=1000)
