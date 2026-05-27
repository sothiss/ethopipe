from datetime import datetime
import pytest
from pydantic import ValidationError
from ethopipe.models import EthologicalObservation

def get_valid_payload() -> dict:
    """Helper to return a valid dictionary matching EthologicalObservation."""
    return {
        "subject_id": "SUB-DOG-99",
        "timestamp": datetime.now(),
        "species": "Canis lupus familiaris",
        "location": "Behavioral Evaluation Lab A",
        "latitude": 42.3601,
        "longitude": -71.0589,
        "behavior_type": "play_bow",
        "behavior_value": "3 occurrences",
        "severity_score": 1,
        "heart_rate": 85,
        "heart_rate_unit": "BPM",
        "body_temp": 38.5,
        "temp_unit": "°C",
        "respiratory_rate": 24,
        "respiratory_rate_unit": "breaths/min",
        "observation_method": "HumanObservation",
        "narrative": "Subject engaged in standard play solicitations with novel playmate; exhibited active play bows."
    }

def test_valid_observation_passes():
    """Verify that a fully compliant payload parses correctly."""
    payload = get_valid_payload()
    obs = EthologicalObservation(**payload)
    assert obs.subject_id == "SUB-DOG-99"
    assert obs.heart_rate == 85
    assert obs.body_temp == 38.5
    assert obs.respiratory_rate == 24
    assert obs.observation_method == "HumanObservation"

def test_strict_type_enforcement():
    """Verify that ConfigDict(strict=True) prevents implicit type coercion."""
    payload = get_valid_payload()
    
    # Attempting to pass heart_rate as a string representation of an integer
    payload["heart_rate"] = "85"
    
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    
    assert "Input should be a valid integer" in str(exc_info.value)

def test_heart_rate_boundaries():
    """Verify veterinary-validated boundaries for heart rate (30-250 BPM)."""
    payload = get_valid_payload()
    
    # Below resting giant-breed threshold
    payload["heart_rate"] = 29
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be greater than or equal to 30" in str(exc_info.value)
    
    # Above extreme puppy exertion threshold
    payload["heart_rate"] = 251
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be less than or equal to 250" in str(exc_info.value)

def test_body_temp_boundaries():
    """Verify veterinary-validated boundaries for body temperature (35.0 - 40.0 °C)."""
    payload = get_valid_payload()
    
    # Below neonatal hypothermia threshold
    payload["body_temp"] = 34.9
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be greater than or equal to 35" in str(exc_info.value)
    
    # Above hyperthermic/fever limit
    payload["body_temp"] = 40.1
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be less than or equal to 40" in str(exc_info.value)

def test_respiratory_rate_boundaries():
    """Verify boundaries for respiratory rate (10-50 breaths/min)."""
    payload = get_valid_payload()
    
    payload["respiratory_rate"] = 9
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be greater than or equal to 10" in str(exc_info.value)
    
    payload["respiratory_rate"] = 51
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be less than or equal to 50" in str(exc_info.value)

def test_severity_score_boundaries():
    """Verify standardized behavior severity scale limits (1-5)."""
    payload = get_valid_payload()
    
    payload["severity_score"] = 0
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be greater than or equal to 1" in str(exc_info.value)
    
    payload["severity_score"] = 6
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be less than or equal to 5" in str(exc_info.value)

def test_behavior_type_controlled_vocabulary():
    """Verify that only standardized motor patterns are accepted."""
    payload = get_valid_payload()
    payload["behavior_type"] = "invalid_behavior_string"
    
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be" in str(exc_info.value)

def test_observation_method_controlled_vocabulary():
    """Verify that basis of record permits only human or machine observations."""
    payload = get_valid_payload()
    payload["observation_method"] = "SpeculativeObservation"
    
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "Input should be 'HumanObservation' or 'MachineObservation'" in str(exc_info.value)
