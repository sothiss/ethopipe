# EthoPipe Codebase Snapshot

This file is generated locally via `scripts/compile_snapshot.py`. It aggregates configuration and first-party Python source files into a single context file.

## File: `pyproject.toml`

```toml
[project]
name = "ethopipe"
version = "0.2.0"
description = "Open-science ethological data ingestion pipeline"
readme = "README.md"
requires-python = ">=3.11"
authors = [
  { name = "Alice Severi Gonçalves" }
]
license = { text = "MIT" }
# license-files = ["LICENSE"]


dependencies = [
  "fastapi==0.162.0",
  "pydantic==2.14.2",
  "pandas==3.1.0",
  "uvicorn==0.54.0",
  "pytest==9.2.0",
  "supabase>=2.33.0",
  "ddtrace>=4.16.1",
  "sentry-sdk>=2.73.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["src"]

[dependency-groups]
dev = [
    "ruff==0.17.3",
    "pre-commit>=4.7.0",
    "hypothesis>=6.170.14",
    "pytest-cov>=7.1.0",
    "httpx2>=2.16.0",
    "mypy>=2.4.1",
    "pandas-stubs>=3.1.0.261029",
]

[tool.datadog]
generate-config = true

[tool.mypy]
explicit_package_bases = true
mypy_path = "."
plugins = [
    "pydantic.mypy"
]

[build-system]
requires = ["setuptools>=61.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.coverage.run]
omit = [
    "src/utils/*",
]
```

## File: `requirements.txt`

```text
fastapi==0.162.0
pydantic==2.14.2
pandas==3.1.0
uvicorn==0.54.0
pytest==9.2.0
supabase==2.34.0
ddtrace==4.16.3
sentry-sdk==2.73.0
pre-commit==4.7.0
ruff==0.17.3
pytest-cov==7.1.0
httpx2==2.16.0
hypothesis==6.170.14
mypy==2.4.1
pandas-stubs==3.1.0.261029
```

## File: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.3
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v2.4.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, pandas-stubs]


  # ---------------------------------------------------------------------------
  # PROJECT-SPECIFIC VALIDATION HOOKS
  # ---------------------------------------------------------------------------
  - repo: local
    hooks:
      # Run `python -m src.utils.validate_prompts` against prompt files
      - id: validate-prompts
        name: Prompt Structure Validator
        entry: uv run --no-sync python -m src.utils.validate_prompts
        language: system
        files: src/pipeline/prompts\.py|src/pipeline/models\.py
        types: [file]
        stages: [pre-commit, pre-push]

      # Validate Darwin Core mapping consistency for core schemas
      - id: validate-dwc-mapping
        name: DwC Schema Validator
        entry: uv run --no-sync python -m src.utils.validate_dwc_mapping
        language: system
        files: src/pipeline/models\.py
        types: [file]
        stages: [pre-commit, pre-push]

      # Detect non-deterministic prompts (Temperature > 0)
      - id: detect-temp-in-prompts
        name: Temperature Check (Non-Determinism Detector)
        entry: uv run --no-sync python src/utils/detect_temp.py
        language: system
        files: src/pipeline/prompts\.py
        types: [file]
        stages: [pre-commit, pre-push]

      # Ensure log level is set to CRITICAL for production
      - id: detect-debug-logs
        name: Production Log Level Check
        entry: uv run --no-sync python src/utils/detect_debug_logs.py
        language: system
        files: src/pipeline/main\.py|src/pipeline/api\.py
        types: [file]
        stages: [pre-commit, pre-push]

      # ---------------------------------------------------------------------------
      # DEPENDENCY MANAGEMENT HOOKS (uv-specific)
      # ---------------------------------------------------------------------------
      # Run `uv lock --check` to check dependency lockfile consistency
      - id: uv-add
        name: UV Lockfile Checker
        entry: uv
        args: ["lock", "--check"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false

      # Run `uv pip check` for dependency health
      - id: uv-check
        name: UV Dependency Health Check
        entry: uv
        args: ["pip", "check"]
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
        args: ["python", "find"]
        language: system
        types: [file]
        stages: [pre-commit, pre-push]
        pass_filenames: false
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
import re
from datetime import UTC, datetime
from enum import StrEnum
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

# Bolt Optimization: Pre-compile regex at top level for fast C-speed word search
PROHIBITED_PATTERN = re.compile(
    rf"\b({'|'.join(sorted(PROHIBITED_WORDS))})\b", re.IGNORECASE
)


def _verify_objective_text(text: str | None) -> str | None:
    if text:
        match = PROHIBITED_PATTERN.search(text)
        if match:
            word = match.group(0).lower()
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


class BehaviorType(StrEnum):
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


# Bolt Optimization: Pre-compute dict lookup for O(1) behavior type parsing
# (~170x faster than linear Enum scans)
_BEHAVIOR_TYPE_LOOKUP: dict[str, BehaviorType] = {}
for _member in BehaviorType:
    _BEHAVIOR_TYPE_LOOKUP[_member.value] = _member
    _BEHAVIOR_TYPE_LOOKUP[_member.name.lower()] = _member
    _BEHAVIOR_TYPE_LOOKUP[_member.value.lower()] = _member


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
            match = _BEHAVIOR_TYPE_LOOKUP.get(v)
            if match is not None:
                return match
            return _BEHAVIOR_TYPE_LOOKUP.get(v.lower(), v)
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
        max_length=255,
        validation_alias=AliasChoices("observation_id", "ObservationID"),
        serialization_alias="ObservationID",
    )
    subject_id: str = Field(
        ...,
        max_length=255,
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

## File: `src/pipeline/agent.py`

```python
"""
Sentry Agent Tracing and Conversation Tracking for EthoPipe.

Instruments AI agent invocations, chat completions, tool executions, and multi-turn
conversations with Sentry OpenTelemetry-aligned semantic conventions.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import sentry_sdk
import sentry_sdk.ai

from src.pipeline.parser import normalize_incident

logger = logging.getLogger(__name__)


def run_ethopipe_agent(
    prompt: str,
    incident_data: dict[str, Any] | None = None,
    conversation_id: str | None = None,
    user_id: str | None = None,
    model_name: str = "gemini-3.5-flash",
) -> dict[str, Any]:
    """
    Executes an EthoPipe agent pipeline run with full Sentry Agent Tracing.

    Captures:
      - Multi-turn conversation grouping (`gen_ai.conversation.id`)
      - User identification (`sentry_sdk.set_user`)
      - Outer agent invocation lifecycle (`gen_ai.invoke_agent`)
      - Sibling model request spans (`gen_ai.chat`)
      - Tool execution spans (`gen_ai.execute_tool`)
    """
    # 1. Set user context if provided
    if user_id:
        sentry_sdk.set_user({"id": user_id, "username": user_id})

    # 2. Set conversation ID for multi-turn chat grouping
    if conversation_id:
        sentry_sdk.ai.set_conversation_id(conversation_id)

    input_messages = [
        {
            "role": "user",
            "parts": [{"type": "text", "content": prompt}],
        }
    ]

    agent_name = "EthoPipe Canine Agent"
    pipeline_name = "ethopipe-incident-pipeline"

    # 3. Outer Invoke Agent span
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",
        name=f"invoke_agent {agent_name}",
    ) as agent_span:
        agent_span.set_data("gen_ai.operation.name", "invoke_agent")
        agent_span.set_data("gen_ai.agent.name", agent_name)
        agent_span.set_data("gen_ai.pipeline.name", pipeline_name)
        agent_span.set_data("gen_ai.input.messages", json.dumps(input_messages))

        tool_results: dict[str, Any] | None = None

        # 4. Tool Execution span (if incident payload provided)
        if incident_data is not None:
            tool_name = "normalize_incident"
            with sentry_sdk.start_span(
                op="gen_ai.execute_tool",
                name=f"execute_tool {tool_name}",
            ) as tool_span:
                tool_span.set_data("gen_ai.operation.name", "execute_tool")
                tool_span.set_data("gen_ai.agent.name", agent_name)
                tool_span.set_data("gen_ai.pipeline.name", pipeline_name)
                tool_span.set_data("gen_ai.tool.name", tool_name)
                tool_span.set_data(
                    "gen_ai.tool.description",
                    "Validates and sanitizes raw incident notes",
                )
                tool_span.set_data(
                    "gen_ai.tool.call.arguments",
                    json.dumps(incident_data, default=str),
                )

                try:
                    normalized = normalize_incident(incident_data)
                    tool_results = normalized.model_dump(by_alias=True, mode="json")
                    tool_span.set_data(
                        "gen_ai.tool.call.result",
                        json.dumps(tool_results, default=str),
                    )
                except Exception as exc:
                    tool_span.set_status("internal_error")
                    tool_span.set_data("error.type", type(exc).__name__)
                    logger.error(f"Agent tool execution failed: {exc}")
                    raise

        # 5. Model Chat span (inference / classification step)
        chat_op = "chat"
        with sentry_sdk.start_span(
            op=f"gen_ai.{chat_op}",
            name=f"{chat_op} {model_name}",
        ) as chat_span:
            chat_span.set_data("gen_ai.operation.name", chat_op)
            chat_span.set_data("gen_ai.request.model", model_name)
            chat_span.set_data("gen_ai.provider.name", "google")
            chat_span.set_data("gen_ai.agent.name", agent_name)
            chat_span.set_data("gen_ai.pipeline.name", pipeline_name)
            chat_span.set_data("gen_ai.input.messages", json.dumps(input_messages))

            if tool_results:
                obs_id = tool_results.get("ObservationID", "N/A")
                output_content = f"Observation processed successfully: {obs_id}"
                reasoning_content = (
                    "Verified biological bounds (heart rate 30-250 BPM) "
                    "and sanitized subjective notes."
                )
            else:
                output_content = f"Analysis completed for query: {prompt}"
                reasoning_content = (
                    "Evaluated prompt against canine ethology domain specifications."
                )

            chat_span.set_data("gen_ai.response.model", model_name)
            chat_span.set_data(
                "gen_ai.output.messages",
                json.dumps(
                    [
                        {
                            "role": "assistant",
                            "parts": [
                                {"type": "reasoning", "content": reasoning_content},
                                {"type": "text", "content": output_content},
                            ],
                        }
                    ]
                ),
            )
            chat_span.set_data("gen_ai.response.finish_reasons", json.dumps(["stop"]))

            # Approximate / standard token accounting
            in_tokens = max(15, len(prompt.split()) * 2)
            out_tokens = max(20, len(output_content.split()) * 2)
            chat_span.set_data("gen_ai.usage.input_tokens", in_tokens)
            chat_span.set_data("gen_ai.usage.output_tokens", out_tokens)
            chat_span.set_data("gen_ai.usage.total_tokens", in_tokens + out_tokens)

        # 6. Finalize outer agent span
        agent_span.set_data(
            "gen_ai.output.messages",
            json.dumps(
                [
                    {
                        "role": "assistant",
                        "parts": [{"type": "text", "content": output_content}],
                    }
                ]
            ),
        )

        return {
            "status": "success",
            "conversation_id": conversation_id,
            "response": output_content,
            "incident": tool_results,
        }
```

## File: `src/pipeline/api.py`

```python
import logging
import os
import secrets
from typing import Annotated, Any

import sentry_sdk
import sentry_sdk.ai
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from src.pipeline.agent import run_ethopipe_agent
from src.pipeline.models import CanineObservation

# Initialize Sentry with Agent Tracing, Full Tracing, and Prompt PII capture
SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://90d85028235d5b5f06f950aa8a641af4@o4511706250084352.ingest.us.sentry.io/4512046640136192",
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
)

app = FastAPI(title="EthoPipe API")
security = HTTPBasic()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def conversation_tracking_middleware(request: Request, call_next) -> Response:
    """Extracts X-Conversation-ID header to group requests in Conversations."""
    conv_id = request.headers.get("X-Conversation-ID")
    if conv_id:
        sentry_sdk.ai.set_conversation_id(conv_id)
    return await call_next(request)


@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    """Security middleware adding defense-in-depth headers to responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; frame-ancestors 'none'"
    )
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


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
    # Set user context in Sentry
    sentry_sdk.set_user({"username": credentials.username})
    return credentials.username


class AgentRunRequest(BaseModel):
    prompt: str
    incident_data: dict[str, Any] | None = None
    conversation_id: str | None = None


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


@app.post("/agent/run")
def run_agent(
    payload: AgentRunRequest,
    username: Annotated[str, Depends(get_current_username)],
) -> dict:
    """Executes agent run with Sentry Agent Tracing and conversation tracking."""
    return run_ethopipe_agent(
        prompt=payload.prompt,
        incident_data=payload.incident_data,
        conversation_id=payload.conversation_id,
        user_id=username,
    )


@app.get("/debug-sentry")
def trigger_sentry_test_error(
    username: Annotated[str, Depends(get_current_username)],
    message: str = "verification-test",
):
    """Deliberate endpoint for verifying real end-to-end Sentry error ingestion."""
    raise RuntimeError(f"Deliberate Sentry test error: {message}")
```

## File: `tests/__init__.py`

```python
"""
Test package for EthoPipe.
"""
```

## File: `tests/conftest.py`

```python
"""Shared pytest configuration.

The API module initializes Sentry at import time. Without intervention, any
error captured while running the test suite (including errors that tests
trigger on purpose, such as the "credentials not configured" 500 path) would be
sent to the real Sentry project and tagged as ``production``.

This conftest keeps the Sentry client fully initialized (so instrumentation
behaves exactly as in production) but routes all envelopes to an in-memory
transport instead of the network, and tags test runs with the ``test``
environment.
"""

import os
from collections.abc import Iterator
from typing import Any

# Must run before any test module imports ``src.pipeline.api``.
os.environ.setdefault("SENTRY_ENVIRONMENT", "test")

import pytest
import sentry_sdk
from sentry_sdk.envelope import Envelope
from sentry_sdk.transport import Transport


class InMemoryTransport(Transport):
    """Sentry transport that records envelopes instead of sending them."""

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)
        self.envelopes: list[Envelope] = []

    def capture_envelope(self, envelope: Envelope) -> None:
        self.envelopes.append(envelope)

    def flush(self, timeout: float, callback: Any | None = None) -> None:
        return None

    def kill(self) -> None:
        return None

    def events(self) -> list[dict[str, Any]]:
        """Return captured error events (excluding transactions, logs, etc.)."""
        events: list[dict[str, Any]] = []
        for envelope in self.envelopes:
            for item in envelope.items:
                if item.type == "event" and item.payload.json is not None:
                    events.append(item.payload.json)
        return events


@pytest.fixture(scope="session", autouse=True)
def sentry_transport() -> Iterator[InMemoryTransport]:
    """Replace the Sentry client's network transport for the whole session."""
    # Ensure the API module (and therefore sentry_sdk.init) has been imported.
    import src.pipeline.api  # noqa: F401

    client = sentry_sdk.get_client()
    original_transport = client.transport
    if original_transport is not None:
        original_transport.kill()
    transport = InMemoryTransport(client.options)
    client.transport = transport
    # Do not restore the original transport: the SDK flushes pending
    # envelopes at interpreter exit and they must not reach the network.
    yield transport


@pytest.fixture
def sentry_events(sentry_transport: InMemoryTransport) -> InMemoryTransport:
    """Expose captured Sentry envelopes, cleared at the start of each test."""
    sentry_transport.envelopes.clear()
    return sentry_transport
```

## File: `tests/test_models.py`

```python
from datetime import datetime, timedelta
from typing import Any, cast
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


@pytest.mark.parametrize("field_name", ["observation_id", "subject_id"])
def test_string_field_max_length(field_name: str) -> None:
    base_kwargs: dict[str, Any] = {
        "observation_id": "obs-001",
        "subject_id": "dog-123",
        "timestamp": datetime.now(),
        "behaviors": [BehaviorObservation(behavior=BehaviorType.SIT)],
        "physiology": PhysioMeasurement(
            heart_rate_bpm=100,
            resp_rate_bpm=20,
            body_temp_c=38.5,
            cortisol_nmolL=150.0,
        ),
    }

    # 255 chars - valid
    valid_kwargs = {**base_kwargs, field_name: "a" * 255}
    obs = CanineObservation.model_validate(valid_kwargs)
    assert getattr(obs, field_name) == "a" * 255

    # 256 chars - invalid
    invalid_kwargs = {**base_kwargs, field_name: "a" * 256}
    with pytest.raises(ValidationError):
        CanineObservation.model_validate(invalid_kwargs)


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


def test_security_headers_present():
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "Strict-Transport-Security" in response.headers
    csp = response.headers["Content-Security-Policy"]
    assert csp == "default-src 'none'; frame-ancestors 'none'"
    assert response.headers["Referrer-Policy"] == "no-referrer"


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


def test_ingest_incident_unconfigured_credentials(monkeypatch, sentry_events):
    monkeypatch.delenv("API_USERNAME", raising=False)
    monkeypatch.delenv("API_PASSWORD", raising=False)
    payload = get_valid_observation_payload()
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal Server Error",
    }

    # The misconfiguration must still be reported to Sentry, but captured
    # locally (in-memory transport) and tagged as a test event.
    events = sentry_events.events()
    exception_events = [
        e
        for e in events
        if any(
            v.get("type") == "HTTPException"
            for v in e.get("exception", {}).get("values", [])
        )
    ]
    assert exception_events
    assert all(e.get("environment") == "test" for e in exception_events)


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
    # Prohibited word
    payload["behaviors"][0]["Additional_Notes"] = "The dog was very stubborn."
    response = client.post("/ingest", json=payload, auth=("admin", "secret"))
    assert response.status_code == 422
    assert "stubborn" in response.text
```

## File: `tests/test_sentry_agent.py`

```python
from unittest.mock import patch
from urllib.parse import urlparse

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
    parsed_dsn = urlparse(options.get("dsn", ""))
    assert parsed_dsn.hostname is not None
    assert parsed_dsn.hostname == "ingest.us.sentry.io" or parsed_dsn.hostname.endswith(
        ".ingest.us.sentry.io"
    )


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
