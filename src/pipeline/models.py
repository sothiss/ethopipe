from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def validate_uuid(v):
    if isinstance(v, str):
        return UUID(v)
    return v


def validate_datetime(v):
    if isinstance(v, str):
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            pass
    return v


class EthologicalIncident(BaseModel):
    model_config = ConfigDict(strict=True)

    animal_id: Annotated[UUID, BeforeValidator(validate_uuid)]
    timestamp: Annotated[datetime, BeforeValidator(validate_datetime)] = Field(
        default_factory=datetime.utcnow
    )
    heart_rate: int = Field(..., gt=0, lt=300)
    behavior_type: str = Field(
        ...,
        pattern=r"^(barks|lunges|cowers|neutral|vocalizing|panting)$",
    )
    handler_notes: str = Field(..., max_length=1000)
