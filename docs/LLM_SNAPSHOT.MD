# EthoPipe Codebase Snapshot

This file is auto-generated on git push. It aggregates all configuration and first-party Python source files into a single context file.

## File: `pyproject.toml`

```toml
[project]
name = "ethopipe"
version = "0.2.0a0"
description = "Open-science ethological data ingestion pipeline"
readme = "README.md"
requires-python = ">=3.11"
authors = [
  { name = "Alice Severi Gonçalves" }
]
license = { text = "MIT" }
# license-files = ["LICENSE"]


dependencies = [
  "fastapi==0.138.1",
  "pydantic==2.13.4",
  "pandas==3.0.3",
  "uvicorn==0.49.0",
  "pytest==9.0.3",
  "supabase>=2.31.0",
  "ddtrace>=4.11.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length = 88
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
ignore = []

[tool.ruff.isort]
known-first-party = ["src"]

[dependency-groups]
dev = [
    "ruff==0.11.0",
    "black==26.3.1",
    "pre-commit>=4.6.0",
    "hypothesis>=6.112.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.28.1",
]

[tool.datadog]
generate-config = true

[build-system]
requires = ["setuptools>=61.0.0", "wheel"]
build-backend = "setuptools.build_meta"



```

## File: `requirements.txt`

```text
fastapi==0.138.1
pydantic==2.13.4
pandas==3.0.3
uvicorn==0.49.0
pytest==9.0.3
pre-commit==4.6.0
black==26.3.1
ruff==0.11.0
pytest-cov==7.1.0
httpx==0.28.1
```

## File: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, pandas-stubs]

  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.10.1
    hooks:
      - id: isort
        args: [ --profile, black ]

  # ---------------------------------------------------------------------------
  # PROJECT-SPECIFIC VALIDATION HOOKS
  # ---------------------------------------------------------------------------
  - repo: local
    hooks:
      # Run `python -m src.utils.validate_prompts` against prompt files
      - id: validate-prompts
        name: Prompt Structure Validator
        entry: python -m src.utils.validate_prompts
        language: system
        files: src/prompts.py|src/prompt_validator.py|src/schemas.py|src/models.py
        types: [file]
        stages: [pre-commit, pre-push, pre-commit]

      # Validate Darwin Core mapping consistency for core schemas
      - id: validate-dwc-mapping
        name: DwC Schema Validator
        entry: python -m src.utils.validate_dwc_mapping
        language: system
        files: src/schemas.py|src/models.py
        types: [file]
        stages: [pre-commit, pre-push, pre-commit]

      # Detect non-deterministic prompts (Temperature > 0)
      - id: detect-temp-in-prompts
        name: Temperature Check (Non-Determinism Detector)
        entry: python src/utils/detect_temp.py
        language: system
        files: src/prompts.py
        types: [file]
        stages: [pre-commit, pre-push, pre-commit]

      # Ensure log level is set to CRITICAL for production
      - id: detect-debug-logs
        name: Production Log Level Check
        entry: python src/utils/detect_debug_logs.py
        language: system
        files: src/config.py|src/data_pipeline.py|src/main.py
        types: [file]
        stages: [pre-commit, pre-push, pre-commit]

      # ---------------------------------------------------------------------------
      # DEPENDENCY MANAGEMENT HOOKS (uv-specific)
      # ---------------------------------------------------------------------------
      # Run `uv add` for missing dependencies in pyproject.toml
      - id: uv-add
        name: UV Dependency Checker
        entry: uv
        args: ["add"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false

      # Run `uv check` for dependency health
      - id: uv-check
        name: UV Dependency Health Check
        entry: uv
        args: ["check", "--preview-features", "check-command"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false

      # Run `uv audit` for security vulnerabilities
      - id: uv-audit
        name: UV Dependency Audit
        entry: uv
        args: ["audit", "--preview-features", "audit-command"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false

      # Ensure Python version matches pyproject.toml
      - id: uv-python-version
        name: Python Version Compliance
        entry: uv
        args: ["python", "--version"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false
```

## File: `code-security.datadog.yaml`

```yaml
schema-version: v1.0
sast:
  global-config:
    ignore-paths:
      - ".venv/"
      - ".env"
  use-rulesets:
    - python-best-practices
    - python-code-style
    - python-django
    - python-flask
    - python-inclusive
    - python-pandas
    - python-security

```

## File: `src/pipeline/__init__.py`

```python
"""
EthoPipe package.
"""
```

## File: `src/pipeline/main.py`

```python
def main():
    print("Environment works")


if __name__ == "__main__":
    main()
```

## File: `src/pipeline/models.py`

```python
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
        validation_alias="dwc:individualID",
        serialization_alias="dwc:individualID",
    )
    event_date: str = Field(
        ...,
        validation_alias="dwc:eventDate",
        serialization_alias="dwc:eventDate",
    )
    measurement_type: str = Field(
        ...,
        validation_alias="dwc:measurementType",
        serialization_alias="dwc:measurementType",
    )
    measurement_value: str = Field(
        ...,
        validation_alias="dwc:measurementValue",
        serialization_alias="dwc:measurementValue",
    )
    basis_of_record: str = Field(
        ...,
        validation_alias="dwc:basisOfRecord",
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
```

## File: `src/pipeline/parser.py`

```python
import re

from src.pipeline.models import PROHIBITED_WORDS, CanineObservation

# Pattern to find prohibited words as full words, case-insensitive
PROHIBITED_PATTERN = re.compile(rf"\b({'|'.join(PROHIBITED_WORDS)})\b", re.IGNORECASE)


def de_bias_text(text: str) -> str:
    """
    Actively delete subjective, anthropomorphic terms from raw notes.
    """
    if not text:
        return text
    # Replace prohibited words with empty string
    cleaned = PROHIBITED_PATTERN.sub("", text)
    # Normalize multiple spaces and strip
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def clean_payload_notes(data: dict) -> dict:
    """
    Recursively clean all free-text fields in the observation payload.
    """
    cleaned = dict(data)

    # Clean top-level context/session fields
    for key in ["context_session", "Context/Session", "context"]:
        if key in cleaned and isinstance(cleaned[key], str):
            cleaned[key] = de_bias_text(cleaned[key])

    # Clean notes in individual behavior observations
    if "behaviors" in cleaned and isinstance(cleaned["behaviors"], list):
        cleaned_behaviors = []
        for beh in cleaned["behaviors"]:
            if isinstance(beh, dict):
                beh_copy = dict(beh)
                for note_key in ["additional_notes", "Additional_Notes"]:
                    if note_key in beh_copy and isinstance(beh_copy[note_key], str):
                        beh_copy[note_key] = de_bias_text(beh_copy[note_key])
                cleaned_behaviors.append(beh_copy)
            else:
                cleaned_behaviors.append(beh)
        cleaned["behaviors"] = cleaned_behaviors

    return cleaned


def normalize_incident(data: dict) -> CanineObservation:
    """
    Validate and normalize an incoming incident payload against CanineObservation.
    Subjective terms are actively removed during parsing.
    """
    cleaned_data = clean_payload_notes(data)
    return CanineObservation(**cleaned_data)
```

## File: `src/pipeline/api.py`

```python
import logging
import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.pipeline.models import CanineObservation

app = FastAPI(title="EthoPipe API")
security = HTTPBasic()
logger = logging.getLogger(__name__)


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    expected_username = os.getenv("API_USERNAME")
    expected_password = os.getenv("API_PASSWORD")

    if not expected_username or not expected_password:
        logger.error("Authentication credentials are not configured on the server")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = expected_username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = expected_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_root() -> dict:
    return {"message": "EthoPipe API is running"}


@app.post("/ingest")
def ingest_incident(
    data: CanineObservation,
    username: Annotated[str, Depends(get_current_username)],
) -> dict:
    return {
        "status": "valid",
        "incident": data.model_dump(by_alias=True),
    }
```

## File: `tests/__init__.py`

```python
"""
Test package for EthoPipe.
"""
```

## File: `tests/test_models.py`

```python
from datetime import datetime, timedelta
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
        ObservationID="obs-001",
        SubjectID="dog-123",
        Timestamp_ISO8601=datetime.now(),
        Location="Lab A",
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
            heart_rate_bpm="100",  # String instead of int
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
        ObservationID="obs-001",
        SubjectID="dog-123",
        Timestamp_ISO8601=datetime.now(),
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
            ObservationID="obs-001",
            SubjectID="dog-123",
            Timestamp_ISO8601=datetime.now(),
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
        ObservationID="obs-001",
        SubjectID="dog-123",
        Timestamp_ISO8601=datetime.now(),
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
            ObservationID="obs-001",
            SubjectID="dog-123",
            Timestamp_ISO8601=datetime.now(),
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
    assert "stubborn" not in notes.lower()
    assert "angry" not in notes.lower()
    assert notes == "The dog was but eventually sat. He seemed ."


def test_darwin_core_mapping() -> None:
    obs = CanineObservation(
        ObservationID="obs-001",
        SubjectID="dog-123",
        Timestamp_ISO8601=datetime(2026, 7, 5, 12, 0, 0),
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
```

## File: `tests/test_api.py`

```python
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
    response = client.post("/ingest", json=payload, auth=("wronguser", "wrongpassword"))
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
    payload["behaviors"][0][
        "Additional_Notes"
    ] = "The dog was very stubborn."  # Prohibited word
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 422
    assert "stubborn" in response.text
```

## File: `tests/test_adversarial_boundaries.py`

```python
import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from src.pipeline.models import (
    BehaviorObservation,
    BehaviorType,
    CanineObservation,
    PhysioMeasurement,
)


@given(st.integers(min_value=-1000, max_value=29))
def test_heart_rate_under_bounds_rejection(invalid_hr):
    """
    Ensure the data pipeline strictly rejects physiological inputs beneath
    the absolute clinical baseline bound of 30 BPM.
    """
    with pytest.raises(ValidationError):
        PhysioMeasurement(
            heart_rate_bpm=invalid_hr,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        )


@given(
    st.text(min_size=1, max_size=500).filter(
        lambda x: not (x.isdigit() or any(char in x for char in ["-", ":", "T", "Z"]))
    )
)
def test_narrative_injector_isolation(messy_text):
    """
    Assert that random token variants, string drifts, and partial text injections
    are safely trapped by the type-enforcement layer instead of breaking execution.
    """
    # Test criteria confirming that invalid schemas cause predictable exceptions
    with pytest.raises(ValidationError):
        CanineObservation(
            observation_id="obs-001",
            subject_id="dog-123",
            timestamp=messy_text,
            behaviors=[
                BehaviorObservation(
                    behavior=BehaviorType.SIT,
                )
            ],
            physiology=PhysioMeasurement(
                heart_rate_bpm=100,
                resp_rate_bpm=20,
                body_temp_c=38.5,
                cortisol_nmolL=150.0,
            ),
        )
```

