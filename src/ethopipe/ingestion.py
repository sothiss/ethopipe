"""Ingestion Engine for EthoPipe to parse and validate files."""

import csv
import json
from datetime import datetime
from typing import Any, Optional
from pydantic import ValidationError
from ethopipe.models import EthologicalObservation, QuarantineRecord


def _pre_process_row(
    raw_row: dict[str, Any], column_mapping: dict[str, str]
) -> dict[str, Any]:
    """Translates raw dict keys and performs type pre-processing to accommodate

    ConfigDict(strict=True) on Pydantic models.
    """
    mapped_row = {}

    # Translate keys based on supplied column mappings
    for src_key, val in raw_row.items():
        dst_key = column_mapping.get(src_key, src_key)
        mapped_row[dst_key] = val

    # Establish physiological/numerical type mappings to avoid strict validation failures
    int_fields = {"heart_rate", "respiratory_rate", "severity_score"}
    float_fields = {"body_temp", "latitude", "longitude", "cortisol_level"}

    for field in int_fields:
        if field in mapped_row:
            val = mapped_row[field]
            if val is not None and val != "":
                try:
                    mapped_row[field] = int(val)
                except (ValueError, TypeError):
                    pass  # Pass along, Pydantic will raise a type validation error
            else:
                mapped_row[field] = None

    for field in float_fields:
        if field in mapped_row:
            val = mapped_row[field]
            if val is not None and val != "":
                try:
                    mapped_row[field] = float(val)
                except (ValueError, TypeError):
                    pass
            else:
                mapped_row[field] = None

    # Enforce safe datetime parsing for timestamps (as strict Pydantic mode expects datetime objects)
    if "timestamp" in mapped_row:
        ts = mapped_row["timestamp"]
        if isinstance(ts, str) and ts != "":
            parsed_dt = None
            for fmt in (
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ):
                try:
                    parsed_dt = datetime.strptime(ts.strip(), fmt)
                    break
                except ValueError:
                    continue
            if parsed_dt:
                mapped_row["timestamp"] = parsed_dt

    # Safe conversion for behavior_value (Union[int, float, str]) to match strict mode when numbers are provided
    if "behavior_value" in mapped_row:
        val = mapped_row["behavior_value"]
        if val is not None and val != "":
            # Try to convert to int first, then float, then keep as string
            try:
                mapped_row["behavior_value"] = int(val)
            except (ValueError, TypeError):
                try:
                    mapped_row["behavior_value"] = float(val)
                except (ValueError, TypeError):
                    pass

    # Strip and normalise string fields
    string_fields = {
        "dog_size_category",
        "cortisol_unit",
        "cortisol_matrix",
        "observation_method",
        "behavior_type_id",
    }
    for field in string_fields:
        if field in mapped_row:
            val = mapped_row[field]
            if isinstance(val, str):
                stripped = val.strip()
                mapped_row[field] = stripped if stripped != "" else None

    # Map Title Case behaviors from the data dictionary to their snake_case canonical values
    BEHAVIOR_CANONICAL = {
        "No Aggression": "no_aggression",
        "Moderate Aggression": "moderate_aggression",
        "Serious Aggression": "serious_aggression",
        "Play Bow": "play_bow",
        "Licking of Lips": "licking_of_lips",
        "Looking Away": "looking_away",
        "Stranger-Directed Aggression": "stranger_directed_aggression",
        "Owner-Directed Aggression": "owner_directed_aggression",
        "Dog-Directed Aggression/Fear": "dog_directed_aggression_fear",
        "Trainability": "trainability",
        "Separation-Related Behavior": "separation_related_behavior",
        "Growling": "growling",
        "Whining": "whining",
        "Panting": "panting",
        "Yawning": "yawning",
        "Avoidance": "avoidance",
        "Lip Licking": "lip_licking",
        "Trembling": "trembling",
        "Pacing": "pacing",
        "Vocalization Whine": "vocalization_whine",
        "Posture Freeze": "posture_freeze",
        "Tail Tuck": "tail_tuck",
        "Avoidance Social": "avoidance_social",
    }
    if "behavior_type" in mapped_row:
        bt = mapped_row["behavior_type"]
        if isinstance(bt, str):
            bt_stripped = bt.strip()
            mapped_row["behavior_type"] = BEHAVIOR_CANONICAL.get(
                bt_stripped, bt_stripped
            )

    return mapped_row


def load_csv(
    file_path: str, column_mapping: dict[str, str]
) -> tuple[list[EthologicalObservation], list[QuarantineRecord]]:
    """Ingests dog records from a CSV file, applies column mapping, validates

    against EthologicalObservation schema, and isolates errant lines.

    Args:
        file_path: Path to the CSV file on the filesystem.
        column_mapping: Translation dictionary mapping raw CSV headers to
          Pydantic model fields.

    Returns:
        tuple[list[EthologicalObservation], list[QuarantineRecord]]:
            1. Validated EthologicalObservation list
            2. Quarantine list of QuarantineRecord objects.
    """
    valid_observations = []
    quarantine: list[QuarantineRecord] = []

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            processed = _pre_process_row(row, column_mapping)
            try:
                observation = EthologicalObservation(**processed)
                valid_observations.append(observation)
            except ValidationError as e:
                errors = [
                    f"{err['loc'][0] if err['loc'] else '__root__'}: {err['msg']}"
                    for err in e.errors()
                ]
                quarantine.append(
                    QuarantineRecord(
                        raw_payload=row,
                        errors=errors,
                        ingested_at=datetime.now(),
                        original_index=idx,
                    )
                )

    return valid_observations, quarantine


def load_json(
    file_path: str, column_mapping: Optional[dict[str, str]] = None
) -> tuple[list[EthologicalObservation], list[QuarantineRecord]]:
    """Ingests dog records from a JSON file, applies column mapping, validates

    against EthologicalObservation schema, and isolates errant objects.

    Args:
        file_path: Path to the JSON file on the filesystem.
        column_mapping: Translation dictionary mapping JSON keys to Pydantic
          model fields.

    Returns:
        tuple[list[EthologicalObservation], list[QuarantineRecord]]:
            1. Validated EthologicalObservation list
            2. Quarantine list of QuarantineRecord objects.
    """
    valid_observations = []
    quarantine: list[QuarantineRecord] = []
    mapping = column_mapping or {}

    with open(file_path, mode="r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            quarantine.append(
                QuarantineRecord(
                    raw_payload={"error": "JSON Decode Error"},
                    errors=[f"JSON parsing failed: {str(e)}"],
                    ingested_at=datetime.now(),
                    original_index=0,
                )
            )
            return [], quarantine

    if not isinstance(data, list):
        quarantine.append(
            QuarantineRecord(
                raw_payload={"error": "Invalid JSON format"},
                errors=["Expected JSON file to contain a list of records"],
                ingested_at=datetime.now(),
                original_index=0,
            )
        )
        return [], quarantine

    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            quarantine.append(
                QuarantineRecord(
                    raw_payload={"item": item},
                    errors=["Expected record to be a JSON object (dict)"],
                    ingested_at=datetime.now(),
                    original_index=idx,
                )
            )
            continue

        processed = _pre_process_row(item, mapping)
        try:
            observation = EthologicalObservation(**processed)
            valid_observations.append(observation)
        except ValidationError as e:
            errors = [
                f"{err['loc'][0] if err['loc'] else '__root__'}: {err['msg']}"
                for err in e.errors()
            ]
            quarantine.append(
                QuarantineRecord(
                    raw_payload=item,
                    errors=errors,
                    ingested_at=datetime.now(),
                    original_index=idx,
                )
            )

    return valid_observations, quarantine
