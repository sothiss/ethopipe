from datetime import UTC, datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

# Prohibited subjective/anthropomorphic terms
PROHIBITED_WORDS = {
    "stubborn",
    "angry",
    "spiteful",
    "vicious",
    "mean",
    "happy",
    "sad",
    "frustrated",
    "guilty",
}


def _verify_objective_text(text: str | None) -> str | None:
    if text:
        import re

        cleaned_words = re.findall(r"\b\w+\b", text.lower())
        for word in cleaned_words:
            if word in PROHIBITED_WORDS:
                raise ValueError(
                    f"Subjective/anthropomorphic term '{word}' "
                    "is prohibited in ethological observations."
                )
    return text


# Legacy model for backward compatibility
class EthologicalIncident(BaseModel):
    model_config = ConfigDict(strict=True)

    animal_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    heart_rate: int = Field(..., gt=0, lt=300)
    behavior_type: str = Field(
        ...,
        pattern=r"^(barks|lunges|cowers|neutral|vocalizing|panting)$",
    )
    handler_notes: str = Field(..., max_length=1000)

    @field_validator("animal_id", mode="before")
    @classmethod
    def parse_uuid(cls, v):
        if isinstance(v, str):
            return UUID(v)
        return v

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_legacy_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError as e:
                raise ValueError(f"Invalid legacy timestamp format: {v}") from e
        return v

    @field_validator("handler_notes", mode="after")
    @classmethod
    def check_objective_notes(cls, v: str) -> str:
        _verify_objective_text(v)
        return v


# New Canine Ethology Data Dictionary models


class BehaviorType(str, Enum):
    # Resting Postures
    LYING = "Lying"
    SITTING = "Sitting"
    STANDING = "Standing"

    # Locomotion
    WALKING_TROTTING = "Walking/Trotting"
    RUNNING_GALLOPING = "Running/Galloping"

    # Affiliative Social
    GREETING_NOSE_TOUCH = "Greeting/Nose Touch"
    INGUINAL_SNIFFING = "Inguinal Sniffing"
    PLAY_BOW = "Play Bow"
    PLAY_BITING = "Play Biting"
    CHORUS_HOWL_RALLY = "Chorus Howl/Rally"

    # Agonistic
    DOMINANT_CONFIDENT_POSTURE = "Dominant/Confident Posture"
    SUBMISSIVE_POSTURE = "Submissive Posture"
    DEFENSIVE_THREAT = "Defensive Threat (Snarl/Growl)"
    OFFENSIVE_AGGRESSION = "Offensive Aggression (Lunge/Bite)"
    FLIGHT_ESCAPE = "Flight/Escape"

    # Maternal / Care-seeking
    WHIMPERING_WHINING = "Whimpering/Whining"
    LICKING_LIPS = "Licking Lips (of another)"
    ROLLING_OVER = "Rolling Over (partly)"

    # Reproductive / Sexual
    MOUNTING = "Mounting"
    COPULATORY_TIE = "Copulatory Tie"
    COURTSHIP = "Courtship"

    # Common shorthand / custom values
    REST = "Rest"
    WALK = "Walk"
    RUN = "Run"
    PLAYBOW = "PlayBow"
    SNIFFING = "Sniffing"
    GROWL = "Growl"
    BARK = "Bark"
    PANT = "Pant"
    EAT = "Eat"
    URINATE = "Urinate"

    # Shorthand lowercase aliases for test integration
    BARKS = "barks"
    LUNGES = "lunges"
    COWERS = "cowers"
    NEUTRAL = "neutral"
    VOCALIZING = "vocalizing"
    PANTING = "panting"
    SIT = "Sit"
    LIE_DOWN = "LieDown"


class BehaviorObservation(BaseModel):
    model_config = ConfigDict(strict=True, populate_by_name=True)

    behavior: BehaviorType = Field(
        ...,
        validation_alias=AliasChoices("behavior", "Behavior"),
        serialization_alias="Behavior",
    )
    intensity: str | None = Field(
        None,
        pattern="^(Low|Moderate|High|NA)$",
        validation_alias=AliasChoices("intensity", "Behav_Intensity"),
        serialization_alias="Behav_Intensity",
    )
    start_time: datetime | None = Field(
        None,
        validation_alias=AliasChoices("start_time", "BehaviorStart"),
        serialization_alias="BehaviorStart",
    )
    end_time: datetime | None = Field(
        None,
        validation_alias=AliasChoices("end_time", "BehaviorEnd"),
        serialization_alias="BehaviorEnd",
    )
    additional_notes: str | None = Field(
        None,
        validation_alias=AliasChoices("additional_notes", "Additional_Notes"),
        serialization_alias="Additional_Notes",
    )

    @field_validator("behavior", mode="before")
    @classmethod
    def parse_behavior_type(cls, v):
        if isinstance(v, str):
            for member in BehaviorType:
                if member.value == v:
                    return member
                if (
                    member.name.lower() == v.lower()
                    or member.value.lower() == v.lower()
                ):
                    return member
        return v

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_obs_times(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError as e:
                raise ValueError(f"Invalid observation time format: {v}") from e
        return v

    @field_validator("additional_notes", mode="after")
    @classmethod
    def check_notes_objectivity(cls, v: str | None) -> str | None:
        return _verify_objective_text(v)

    @model_validator(mode="after")
    def validate_duration(self) -> "BehaviorObservation":
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time < self.start_time
        ):
            raise ValueError("end_time must be >= start_time")
        return self


class PhysioMeasurement(BaseModel):
    model_config = ConfigDict(strict=True, populate_by_name=True)

    heart_rate_bpm: int = Field(
        ...,
        ge=30,
        le=250,
        validation_alias=AliasChoices("heart_rate_bpm", "HeartRate_BPM"),
        serialization_alias="HeartRate_BPM",
    )
    resp_rate_bpm: int = Field(
        ...,
        ge=0,
        le=200,
        validation_alias=AliasChoices("resp_rate_bpm", "RespRate_BPM"),
        serialization_alias="RespRate_BPM",
    )
    body_temp_c: float = Field(
        ...,
        ge=36.0,
        le=41.0,
        validation_alias=AliasChoices("body_temp_c", "BodyTemp_C"),
        serialization_alias="BodyTemp_C",
    )
    cortisol_nmolL: float = Field(
        ...,
        ge=0.0,
        le=600.0,
        validation_alias=AliasChoices("cortisol_nmolL", "Cortisol_nmolL"),
        serialization_alias="Cortisol_nmolL",
    )
    other_biomarkers: dict[str, float] | None = Field(
        None,
        validation_alias=AliasChoices("other_biomarkers", "OtherBiomarkers"),
        serialization_alias="OtherBiomarkers",
    )


class MeasurementOrFact(BaseModel):
    model_config = ConfigDict(strict=True, populate_by_name=True)

    individual_id: str = Field(
        ...,
        validation_alias=AliasChoices("individual_id", "dwc:individualID"),
        serialization_alias="dwc:individualID",
    )
    event_date: str = Field(
        ...,
        validation_alias=AliasChoices("event_date", "dwc:eventDate"),
        serialization_alias="dwc:eventDate",
    )
    measurement_type: str = Field(
        ...,
        validation_alias=AliasChoices("measurement_type", "dwc:measurementType"),
        serialization_alias="dwc:measurementType",
    )
    measurement_value: str = Field(
        ...,
        validation_alias=AliasChoices("measurement_value", "dwc:measurementValue"),
        serialization_alias="dwc:measurementValue",
    )
    basis_of_record: str = Field(
        ...,
        validation_alias=AliasChoices("basis_of_record", "dwc:basisOfRecord"),
        serialization_alias="dwc:basisOfRecord",
    )


class CanineObservation(BaseModel):
    model_config = ConfigDict(strict=True, populate_by_name=True)

    observation_id: str = Field(
        ...,
        validation_alias=AliasChoices("observation_id", "ObservationID"),
        serialization_alias="ObservationID",
    )
    subject_id: str = Field(
        ...,
        validation_alias=AliasChoices("subject_id", "SubjectID"),
        serialization_alias="SubjectID",
    )
    timestamp: datetime = Field(
        ...,
        validation_alias=AliasChoices("timestamp", "Timestamp_ISO8601"),
        serialization_alias="Timestamp_ISO8601",
    )
    location: str | None = Field(
        None,
        validation_alias=AliasChoices("location", "Location"),
        serialization_alias="Location",
    )
    context_session: str | None = Field(
        None,
        validation_alias=AliasChoices("context_session", "Context/Session", "context"),
        serialization_alias="Context/Session",
    )
    behaviors: list[BehaviorObservation] = Field(..., min_length=1)
    physiology: PhysioMeasurement
    dog_size: Literal["Toy", "Giant", "Standard"] | None = Field(
        None,
        validation_alias=AliasChoices("dog_size", "DogSize"),
        serialization_alias="DogSize",
    )

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_obs_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError as e:
                raise ValueError(f"Invalid observation timestamp format: {v}") from e
        return v

    @field_validator("context_session", mode="after")
    @classmethod
    def check_context_objectivity(cls, v: str | None) -> str | None:
        return _verify_objective_text(v)

    @model_validator(mode="after")
    def validate_heart_rate_limits(self) -> "CanineObservation":
        if self.physiology and self.physiology.heart_rate_bpm is not None:
            hr = self.physiology.heart_rate_bpm
            if self.dog_size == "Toy" and not (80 <= hr <= 200):
                raise ValueError(
                    f"Heart rate {hr} BPM is out of bounds for Toy (80-200 BPM)"
                )
            if self.dog_size == "Giant" and not (40 <= hr <= 110):
                raise ValueError(
                    f"Heart rate {hr} BPM is out of bounds for Giant (40-110 BPM)"
                )
        return self

    def to_dwc(self) -> list[MeasurementOrFact]:
        records = []
        event_date_str = self.timestamp.isoformat()

        # Map behaviors to MeasurementOrFact
        for ob in self.behaviors:
            records.append(
                MeasurementOrFact(
                    individual_id=self.subject_id,
                    event_date=event_date_str,
                    measurement_type=ob.behavior.value,
                    measurement_value=ob.intensity or "observed",
                    basis_of_record="HumanObservation",
                )
            )

        # Map physiology to MeasurementOrFact
        if self.physiology:
            phys = self.physiology
            if phys.heart_rate_bpm is not None:
                records.append(
                    MeasurementOrFact(
                        individual_id=self.subject_id,
                        event_date=event_date_str,
                        measurement_type="heart_rate_bpm",
                        measurement_value=str(phys.heart_rate_bpm),
                        basis_of_record="MachineObservation",
                    )
                )
            if phys.resp_rate_bpm is not None:
                records.append(
                    MeasurementOrFact(
                        individual_id=self.subject_id,
                        event_date=event_date_str,
                        measurement_type="resp_rate_bpm",
                        measurement_value=str(phys.resp_rate_bpm),
                        basis_of_record="MachineObservation",
                    )
                )
            if phys.body_temp_c is not None:
                records.append(
                    MeasurementOrFact(
                        individual_id=self.subject_id,
                        event_date=event_date_str,
                        measurement_type="body_temp_c",
                        measurement_value=str(phys.body_temp_c),
                        basis_of_record="MachineObservation",
                    )
                )
            if phys.cortisol_nmolL is not None:
                records.append(
                    MeasurementOrFact(
                        individual_id=self.subject_id,
                        event_date=event_date_str,
                        measurement_type="cortisol_nmolL",
                        measurement_value=str(phys.cortisol_nmolL),
                        basis_of_record="MachineObservation",
                    )
                )

        return records
