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
        "narrative": "Subject engaged in standard play solicitations with novel playmate; exhibited active play bows.",
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
    assert "Input should be 'HumanObservation' or 'MachineObservation'" in str(
        exc_info.value
    )


def test_size_adjusted_heart_rate():
    """Verify that size-adjusted heart rate bounds are strictly enforced by model_validator."""
    payload = get_valid_payload()

    # Toy dog: limit is 80 - 200 BPM
    payload["dog_size_category"] = "Toy"

    # Under boundary
    payload["heart_rate"] = 79
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "out of veterinary bounds" in str(exc_info.value)

    # Over boundary
    payload["heart_rate"] = 201
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "out of veterinary bounds" in str(exc_info.value)

    # Within bounds should pass
    payload["heart_rate"] = 150
    obs = EthologicalObservation(**payload)
    assert obs.heart_rate == 150

    # Giant dog: limit is 40 - 110 BPM
    payload["dog_size_category"] = "Giant"

    # Under boundary
    payload["heart_rate"] = 39
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "out of veterinary bounds" in str(exc_info.value)

    # Over boundary
    payload["heart_rate"] = 111
    with pytest.raises(ValidationError) as exc_info:
        EthologicalObservation(**payload)
    assert "out of veterinary bounds" in str(exc_info.value)

    # Within bounds should pass
    payload["heart_rate"] = 65
    obs = EthologicalObservation(**payload)
    assert obs.heart_rate == 65


def test_cortisol_validation():
    """Verify validation boundaries and matrix types for cortisol biomarker measurements."""
    payload = get_valid_payload()

    # Valid cortisol payload
    payload["cortisol_level"] = 3.5
    payload["cortisol_matrix"] = "saliva"
    obs = EthologicalObservation(**payload)
    assert obs.cortisol_level == 3.5
    assert obs.cortisol_matrix == "saliva"
    assert obs.cortisol_unit == "ng/mL"

    # Negative cortisol level is invalid
    payload["cortisol_level"] = -0.1
    with pytest.raises(ValidationError):
        EthologicalObservation(**payload)

    # Invalid cortisol matrix is rejected
    payload["cortisol_level"] = 2.0
    payload["cortisol_matrix"] = "invalid_matrix"
    with pytest.raises(ValidationError):
        EthologicalObservation(**payload)


def test_expanded_behavior_controlled_vocabulary():
    """Verify that all new data dictionary behaviors are validated correctly."""
    payload = get_valid_payload()

    # Newly added behavioral terms (Title Case and snake_case)
    new_behaviors = [
        "No Aggression",
        "no_aggression",
        "Moderate Aggression",
        "moderate_aggression",
        "Serious Aggression",
        "serious_aggression",
        "Stranger-Directed Aggression",
        "stranger_directed_aggression",
        "Owner-Directed Aggression",
        "owner_directed_aggression",
        "Dog-Directed Aggression/Fear",
        "dog_directed_aggression_fear",
        "Trainability",
        "trainability",
        "Separation-Related Behavior",
        "separation_related_behavior",
    ]

    for behavior in new_behaviors:
        payload["behavior_type"] = behavior
        obs = EthologicalObservation(**payload)
        assert obs.behavior_type == behavior


def test_automatic_behavior_ontology_resolution():
    """Verify that the model auto-populates behavior_type_id using BEHAVIOR_ONTOLOGY_MAPPING."""
    payload = get_valid_payload()

    # 1. Test standard 'barks' vocalization
    payload["behavior_type"] = "barks"
    payload["behavior_type_id"] = None
    obs = EthologicalObservation(**payload)
    assert obs.behavior_type_id == "http://purl.obolibrary.org/obo/GO_0071625"

    # 2. Test standard 'play_bow' behavior
    payload["behavior_type"] = "play_bow"
    obs = EthologicalObservation(**payload)
    assert obs.behavior_type_id == "http://purl.obolibrary.org/obo/NBO_0000109"

    # 3. Test Title Case behavior
    payload["behavior_type"] = "Stranger-Directed Aggression"
    obs = EthologicalObservation(**payload)
    assert obs.behavior_type_id == "http://purl.obolibrary.org/obo/GO_0002118"


def test_explicit_behavior_ontology_override():
    """Verify that passing an explicit behavior_type_id overrides default mapping."""
    payload = get_valid_payload()
    payload["behavior_type"] = "barks"
    payload["behavior_type_id"] = "http://example.org/custom_bark_ontology_id"

    obs = EthologicalObservation(**payload)
    assert obs.behavior_type_id == "http://example.org/custom_bark_ontology_id"


def test_new_vocabulary_behaviors_validation_and_resolution():
    """Verify validation and ontology resolution for the newly added behaviors."""
    payload = get_valid_payload()

    test_cases = [
        ("growling", "Growling", "http://purl.obolibrary.org/obo/GO_0071625"),
        ("whining", "Whining", "http://purl.obolibrary.org/obo/GO_0071625"),
        ("panting", "Panting", "http://purl.obolibrary.org/obo/GO_0001659"),
        ("yawning", "Yawning", "http://purl.obolibrary.org/obo/NBO_0000074"),
        ("avoidance", "Avoidance", "http://purl.obolibrary.org/obo/NBO_0000635"),
        ("lip_licking", "Lip Licking", "http://purl.obolibrary.org/obo/NBO_0000216"),
        ("trembling", "Trembling", "http://purl.obolibrary.org/obo/VT_0002236"),
        ("pacing", "Pacing", "http://purl.obolibrary.org/obo/NBO_0000100"),
        (
            "vocalization_whine",
            "Vocalization Whine",
            "http://purl.obolibrary.org/obo/NBO_0000233",
        ),
        (
            "posture_freeze",
            "Posture Freeze",
            "http://purl.obolibrary.org/obo/NBO_0000282",
        ),
        ("tail_tuck", "Tail Tuck", "http://purl.obolibrary.org/obo/VT_0000030"),
        (
            "avoidance_social",
            "Avoidance Social",
            "http://purl.obolibrary.org/obo/NBO_0000171",
        ),
    ]

    for canonical, title_case, expected_uri in test_cases:
        # Canonical validation and resolution
        payload["behavior_type"] = canonical
        payload["behavior_type_id"] = None
        obs = EthologicalObservation(**payload)
        assert obs.behavior_type == canonical
        assert obs.behavior_type_id == expected_uri

        # Title Case validation and resolution
        payload["behavior_type"] = title_case
        payload["behavior_type_id"] = None
        obs_title = EthologicalObservation(**payload)
        assert obs_title.behavior_type == title_case
        assert obs_title.behavior_type_id == expected_uri


def test_canonical_behavior_semantic_models():
    """Verify that CanonicalBehavior enum and associated semantic models validate correctly."""
    from ethopipe.models import (
        CanonicalBehavior,
        BehavioralObservation,
        EthogramExtractionLog,
    )

    # Check Enum elements
    assert CanonicalBehavior.LIP_LICKING == "lip_licking"
    assert CanonicalBehavior.TREMBLING == "trembling"
    assert CanonicalBehavior.PACING == "pacing"
    assert CanonicalBehavior.VOCALIZATION_WHINE == "vocalization_whine"
    assert CanonicalBehavior.POSTURE_FREEZE == "posture_freeze"
    assert CanonicalBehavior.PANTING == "panting"
    assert CanonicalBehavior.TAIL_TUCK == "tail_tuck"
    assert CanonicalBehavior.AVOIDANCE_SOCIAL == "avoidance_social"

    # Valid BehavioralObservation payload
    obs_payload = {
        "behavior": "lip_licking",
        "ontology_uri": "NBO:0000216",
        "source_text": "Subject was licking lips",
        "confidence_score": 0.95,
    }

    obs = BehavioralObservation(**obs_payload)
    assert obs.behavior == CanonicalBehavior.LIP_LICKING
    assert obs.ontology_uri == "NBO:0000216"
    assert obs.confidence_score == 0.95

    # Invalid confidence score raises ValidationError
    obs_payload["confidence_score"] = 1.05
    with pytest.raises(ValidationError):
        BehavioralObservation(**obs_payload)

    # Valid EthogramExtractionLog payload
    log_payload = {
        "observations": [
            {
                "behavior": "posture_freeze",
                "ontology_uri": "NBO:0000282",
                "source_text": "Subject froze stiffly",
                "confidence_score": 0.88,
            },
            {
                "behavior": "tail_tuck",
                "ontology_uri": "VT:0000030",
                "source_text": "dog tucked its tail",
                "confidence_score": 0.90,
            },
        ]
    }

    log = EthogramExtractionLog(**log_payload)
    assert len(log.observations) == 2
    assert log.observations[0].behavior == CanonicalBehavior.POSTURE_FREEZE
    assert log.observations[1].behavior == CanonicalBehavior.TAIL_TUCK


def test_quarantine_record_validation():
    """Verify that QuarantineRecord validates successfully and enforces strict types."""
    from ethopipe.models import QuarantineRecord

    payload = {
        "raw_payload": {"subject_id": "DOG1", "heart_rate": "invalid_hr"},
        "errors": ["heart_rate: Input should be a valid integer"],
        "ingested_at": datetime.now(),
        "original_index": 5,
    }

    rec = QuarantineRecord(**payload)
    assert rec.raw_payload == {"subject_id": "DOG1", "heart_rate": "invalid_hr"}
    assert len(rec.errors) == 1
    assert rec.errors[0] == "heart_rate: Input should be a valid integer"
    assert rec.original_index == 5

    # Test type enforcement
    payload["original_index"] = "not-an-int"
    with pytest.raises(ValidationError):
        QuarantineRecord(**payload)
