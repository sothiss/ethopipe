import json
from datetime import datetime
import pytest
from ethopipe.ingestion import load_csv, load_json

@pytest.fixture
def column_mapping() -> dict[str, str]:
    return {
        "DogID": "subject_id",
        "LocalTime": "timestamp",
        "Locality": "location",
        "Behavior": "behavior_type",
        "Value": "behavior_value",
        "Rating": "severity_score",
        "HeartRateBPM": "heart_rate",
        "RecordBasis": "observation_method",
        "Notes": "narrative",
        "DogSizeCategory": "dog_size_category",
        "CortisolLevel": "cortisol_level",
        "CortisolUnit": "cortisol_unit",
        "CortisolMatrix": "cortisol_matrix"
    }

def test_load_csv_valid(tmp_path, column_mapping):
    """Verify that a well-formed CSV file is successfully ingested and translated."""
    csv_content = (
        "DogID,LocalTime,Locality,Behavior,Value,Rating,HeartRateBPM,RecordBasis,Notes\n"
        "SUB-DOG-01,2026-05-27T10:00:00,Facility Yard A,barks,5,2,95,HumanObservation,Observed barking at fence.\n"
        "SUB-DOG-02,2026-05-27 10:15:00,Facility Yard B,play_bow,2,,78,HumanObservation,Play solicitations observed.\n"
    )
    csv_file = tmp_path / "test_valid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    valid_obs, quarantine = load_csv(str(csv_file), column_mapping)

    assert len(quarantine) == 0
    assert len(valid_obs) == 2

    # Row 1 check
    assert valid_obs[0].subject_id == "SUB-DOG-01"
    assert isinstance(valid_obs[0].timestamp, datetime)
    assert valid_obs[0].timestamp.hour == 10
    assert valid_obs[0].location == "Facility Yard A"
    assert valid_obs[0].behavior_type == "barks"
    assert valid_obs[0].behavior_value == 5
    assert valid_obs[0].severity_score == 2
    assert valid_obs[0].heart_rate == 95
    assert valid_obs[0].observation_method == "HumanObservation"
    assert valid_obs[0].narrative == "Observed barking at fence."

    # Row 2 check (valid even with empty optional severity_score)
    assert valid_obs[1].subject_id == "SUB-DOG-02"
    assert valid_obs[1].severity_score is None
    assert valid_obs[1].heart_rate == 78

def test_load_csv_quarantine(tmp_path, column_mapping):
    """Verify that malformed rows in a CSV are quarantined without halting ingestion."""
    csv_content = (
        "DogID,LocalTime,Locality,Behavior,Value,Rating,HeartRateBPM,RecordBasis,Notes\n"
        "SUB-DOG-01,2026-05-27T10:00:00,Yard,barks,5,2,95,HumanObservation,Valid row.\n"
        "SUB-DOG-02,2026-05-27T10:00:00,Yard,invalid_vocab,5,2,95,HumanObservation,Bad behavior type.\n"
        "SUB-DOG-03,2026-05-27T10:00:00,Yard,barks,5,2,20,HumanObservation,Heart rate below threshold.\n"
        "SUB-DOG-04,2026-05-27T10:00:00,Yard,barks,5,2,high,HumanObservation,Non-numeric heart rate.\n"
        "SUB-DOG-05,2026-05-27T10:00:00,Yard,barks,5,2,110,HumanObservation,Valid row.\n"
    )
    csv_file = tmp_path / "test_quarantine.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    valid_obs, quarantine = load_csv(str(csv_file), column_mapping)

    # Valid rows 1 and 5 should be accepted
    assert len(valid_obs) == 2
    assert valid_obs[0].subject_id == "SUB-DOG-01"
    assert valid_obs[1].subject_id == "SUB-DOG-05"

    # Errant rows 2, 3, and 4 should be quarantined
    assert len(quarantine) == 3
    assert 2 in quarantine
    assert 3 in quarantine
    assert 4 in quarantine

    # Verify descriptions in quarantine logs
    assert any("behavior_type" in err for err in quarantine[2])
    assert any("heart_rate" in err for err in quarantine[3])
    assert any("heart_rate" in err for err in quarantine[4])

def test_load_json_valid(tmp_path, column_mapping):
    """Verify that a standard JSON list is successfully parsed and validated."""
    json_data = [
        {
            "DogID": "SUB-DOG-10",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "cowers",
            "Value": "10s",
            "Rating": 3,
            "HeartRateBPM": 140,
            "RecordBasis": "HumanObservation",
            "Notes": "Subject cowered behind observer for 10 seconds."
        },
        {
            "DogID": "SUB-DOG-11",
            "LocalTime": "2026-05-27T12:05:00",
            "Locality": "Room C",
            "Behavior": "neutral",
            "Value": "continuous",
            "Rating": 1,
            "HeartRateBPM": 72,
            "RecordBasis": "HumanObservation",
            "Notes": "Relaxed body posture."
        }
    ]
    json_file = tmp_path / "test_valid.json"
    json_file.write_text(json.dumps(json_data), encoding="utf-8")

    valid_obs, quarantine = load_json(str(json_file), column_mapping)

    assert len(quarantine) == 0
    assert len(valid_obs) == 2
    assert valid_obs[0].subject_id == "SUB-DOG-10"
    assert valid_obs[1].subject_id == "SUB-DOG-11"

def test_load_json_quarantine(tmp_path, column_mapping):
    """Verify that bad elements in a JSON array are isolated and logged."""
    json_data = [
        {
            "DogID": "SUB-DOG-10",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "cowers",
            "Value": "10s",
            "Rating": 3,
            "HeartRateBPM": 140,
            "RecordBasis": "HumanObservation",
            "Notes": "Valid row."
        },
        "not-a-dict-item",  # Should trigger non-dict quarantine
        {
            "DogID": "SUB-DOG-12",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "cowers",
            "Value": "10s",
            "Rating": 3,
            "HeartRateBPM": 260,  # HR too high
            "RecordBasis": "HumanObservation",
            "Notes": "Bad HR."
        }
    ]
    json_file = tmp_path / "test_quarantine.json"
    json_file.write_text(json.dumps(json_data), encoding="utf-8")

    valid_obs, quarantine = load_json(str(json_file), column_mapping)

    assert len(valid_obs) == 1
    assert valid_obs[0].subject_id == "SUB-DOG-10"

    assert len(quarantine) == 2
    assert quarantine[2] == ["Expected record to be a JSON object (dict)"]
    assert any("heart_rate" in err for err in quarantine[3])

def test_load_json_corrupted(tmp_path):
    """Verify that completely unparseable JSON files return a file-level error."""
    json_file = tmp_path / "corrupted.json"
    json_file.write_text("{invalid-json-schema", encoding="utf-8")

    valid_obs, quarantine = load_json(str(json_file))
    
    assert len(valid_obs) == 0
    assert 0 in quarantine
    assert any("JSON parsing failed" in err for err in quarantine[0])

def test_load_csv_data_dictionary_integration(tmp_path, column_mapping):
    """Verify end-to-end CSV ingestion with size category, cortisol levels, and Title Case normalisation."""
    csv_content = (
        "DogID,LocalTime,Locality,Behavior,Value,Rating,HeartRateBPM,RecordBasis,Notes,DogSizeCategory,CortisolLevel,CortisolMatrix\n"
        "SUB-DOG-50,2026-05-27T10:00:00,Yard,No Aggression,1,1,85,HumanObservation,Observed no aggression.,Toy,2.4,saliva\n"
        "SUB-DOG-51,2026-05-27T10:00:00,Yard,Licking of Lips,3,2,195,HumanObservation,Stressed licking.,Toy,3.1,saliva\n"
        "SUB-DOG-52,2026-05-27T10:00:00,Yard,Play Bow,2,1,75,HumanObservation,Toy dog with too low HR.,Toy,1.8,saliva\n"
    )
    csv_file = tmp_path / "test_data_dict.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    valid_obs, quarantine = load_csv(str(csv_file), column_mapping)

    # Valid rows 1 and 2 should pass
    # Row 3 (SUB-DOG-52) is a Toy dog with HR 75 BPM, which is below the size-adjusted min limit of 80 BPM! Should be quarantined.
    assert len(valid_obs) == 2
    assert len(quarantine) == 1
    assert 3 in quarantine
    assert any("out of veterinary bounds" in err for err in quarantine[3])

    # Assert Title Case behavior was successfully canonicalized to snake_case in _pre_process_row
    assert valid_obs[0].behavior_type == "no_aggression"
    assert valid_obs[0].dog_size_category == "Toy"
    assert valid_obs[0].cortisol_level == 2.4
    assert valid_obs[0].cortisol_matrix == "saliva"

    assert valid_obs[1].behavior_type == "licking_of_lips"
    assert valid_obs[1].heart_rate == 195

def test_load_json_data_dictionary_integration(tmp_path, column_mapping):
    """Verify end-to-end JSON ingestion with size category, cortisol levels, and Title Case normalisation."""
    json_data = [
        {
            "DogID": "SUB-DOG-60",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "Stranger-Directed Aggression",
            "Value": "1 occurrence",
            "Rating": 3,
            "HeartRateBPM": 60,
            "RecordBasis": "HumanObservation",
            "Notes": "Growled at stranger.",
            "DogSizeCategory": "Giant",
            "CortisolLevel": "1.2",
            "CortisolMatrix": "hair"
        },
        {
            "DogID": "SUB-DOG-61",
            "LocalTime": "2026-05-27T12:00:00",
            "Locality": "Room C",
            "Behavior": "Play Bow",
            "Value": "2 bows",
            "Rating": 1,
            "HeartRateBPM": 120, # Giant dog with HR 120 (max for Giant is 110)
            "RecordBasis": "HumanObservation",
            "Notes": "Too high HR for Giant.",
            "DogSizeCategory": "Giant",
            "CortisolLevel": "0.8",
            "CortisolMatrix": "hair"
        }
    ]
    json_file = tmp_path / "test_data_dict.json"
    json_file.write_text(json.dumps(json_data), encoding="utf-8")

    valid_obs, quarantine = load_json(str(json_file), column_mapping)

    # SUB-DOG-60 should pass (HR 60 is within Giant bounds 40-110)
    # SUB-DOG-61 should be quarantined (HR 120 is above Giant bounds 40-110)
    assert len(valid_obs) == 1
    assert len(quarantine) == 1
    assert 2 in quarantine
    assert any("out of veterinary bounds" in err for err in quarantine[2])

    assert valid_obs[0].subject_id == "SUB-DOG-60"
    assert valid_obs[0].behavior_type == "stranger_directed_aggression"
    assert valid_obs[0].cortisol_level == 1.2
    assert valid_obs[0].cortisol_matrix == "hair"

