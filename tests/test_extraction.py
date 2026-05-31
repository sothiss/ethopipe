from datetime import datetime

from ethopipe.extraction import extract_from_narrative
from ethopipe.models import EthologicalObservation


def test_vitals_extraction():
    """Verify correct parsing of physiological vitals, cortisol levels, matrix, and severity score."""
    narrative = (
        "Subject showed high anxiety. Heart rate: 95 BPM, body temp recorded at 38.4 C. "
        "Respiratory rate is 18 breaths/min. Saliva cortisol concentration: 2.4 ng/mL. "
        "Severity score of 4."
    )
    ts = datetime.now()

    obs_list = extract_from_narrative(
        narrative=narrative,
        subject_id="SUB-DOG-701",
        timestamp=ts,
        location="Facility Yard A",
        dog_size_category="Medium"
    )

    # Since no explicit behavior was matched, it falls back to 'neutral' to record vitals
    assert len(obs_list) == 1
    obs = obs_list[0]

    assert obs.subject_id == "SUB-DOG-701"
    assert obs.timestamp == ts
    assert obs.location == "Facility Yard A"
    assert obs.behavior_type == "neutral"
    assert obs.behavior_value == 1
    assert obs.heart_rate == 95
    assert obs.body_temp == 38.4
    assert obs.respiratory_rate == 18
    assert obs.cortisol_level == 2.4
    assert obs.cortisol_matrix == "saliva"
    assert obs.severity_score == 4


def test_stemmed_behavior_and_frequency():
    """Verify that word stem conjugations map to canonical terms and resolve frequency counts."""
    ts = datetime.now()

    # Test Case 1: Growled twice (Verb stemming + written count)
    obs_1 = extract_from_narrative(
        "Subject growled twice.", "SUB-DOG-702", ts, "Room A"
    )
    assert len(obs_1) == 1
    assert obs_1[0].behavior_type == "growling"
    assert obs_1[0].behavior_value == 2

    # Test Case 2: Barked 5 times (Verb stemming + numeric count)
    obs_2 = extract_from_narrative(
        "Subject barked 5 times.", "SUB-DOG-702", ts, "Room A"
    )
    assert len(obs_2) == 1
    assert obs_2[0].behavior_type == "barks"
    assert obs_2[0].behavior_value == 5

    # Test Case 3: Play bow once (Multi-word + written count)
    obs_3 = extract_from_narrative(
        "Exhibited play bow once.", "SUB-DOG-702", ts, "Room A"
    )
    assert len(obs_3) == 1
    assert obs_3[0].behavior_type == "play_bow"
    assert obs_3[0].behavior_value == 1

    # Test Case 4: Licked lips continuous (Synonym stem + continuous string)
    obs_4 = extract_from_narrative(
        "Licked lips continuously.", "SUB-DOG-702", ts, "Room A"
    )
    assert len(obs_4) == 1
    assert obs_4[0].behavior_type == "licking_of_lips"
    assert obs_4[0].behavior_value == "continuous"


def test_multiple_behaviors_extraction():
    """Verify that narratives containing multiple behaviors correctly emit distinct observations."""
    narrative = (
        "Subject small dog barked twice, then lunged 3 times. "
        "Heart rate: 110 BPM. Severity score of 4."
    )
    ts = datetime.now()

    obs_list = extract_from_narrative(
        narrative=narrative,
        subject_id="SUB-DOG-703",
        timestamp=ts,
        location="Facility Yard B",
        dog_size_category="Small"
    )

    # Asserts that two unique observations were extracted and created
    assert len(obs_list) == 2

    # Sort to ensure order matches assertions
    obs_list.sort(key=lambda o: o.behavior_type)

    # First observation should be 'barks' (value 2)
    assert obs_list[0].behavior_type == "barks"
    assert obs_list[0].behavior_value == 2
    assert obs_list[0].heart_rate == 110
    assert obs_list[0].severity_score == 4
    assert obs_list[0].dog_size_category == "Small"

    # Second observation should be 'lunges' (value 3)
    assert obs_list[1].behavior_type == "lunges"
    assert obs_list[1].behavior_value == 3
    assert obs_list[1].heart_rate == 110
    assert obs_list[1].severity_score == 4
    assert obs_list[1].dog_size_category == "Small"


def test_new_canonical_behaviors_extraction():
    """Verify narrative extraction and normalization for the new canonical canine behaviors."""
    ts = datetime.now()

    # Trembling (continuous)
    obs_tremble = extract_from_narrative(
        "Subject dog was trembling continuously.", "SUB-DOG-704", ts, "Room B"
    )
    assert len(obs_tremble) == 1
    assert obs_tremble[0].behavior_type == "trembling"
    assert obs_tremble[0].behavior_value == "continuous"
    assert obs_tremble[0].behavior_type_id == "http://purl.obolibrary.org/obo/VT_0002236"

    # Pacing (numeric count)
    obs_pacing = extract_from_narrative(
        "Canine paced twice in circle.", "SUB-DOG-704", ts, "Room B"
    )
    assert len(obs_pacing) == 1
    assert obs_pacing[0].behavior_type == "pacing"
    assert obs_pacing[0].behavior_value == 2
    assert obs_pacing[0].behavior_type_id == "http://purl.obolibrary.org/obo/NBO_0000100"

    # Posture Freeze (written count)
    obs_freeze = extract_from_narrative(
        "Subject exhibited posture freeze once.", "SUB-DOG-704", ts, "Room B"
    )
    assert len(obs_freeze) == 1
    assert obs_freeze[0].behavior_type == "posture_freeze"
    assert obs_freeze[0].behavior_value == 1
    assert obs_freeze[0].behavior_type_id == "http://purl.obolibrary.org/obo/NBO_0000282"

    # Tail Tuck (thrice)
    obs_tail = extract_from_narrative(
        "Tail tucked thrice when barrier removed.", "SUB-DOG-704", ts, "Room B"
    )
    assert len(obs_tail) == 1
    assert obs_tail[0].behavior_type == "tail_tuck"
    assert obs_tail[0].behavior_value == 3
    assert obs_tail[0].behavior_type_id == "http://purl.obolibrary.org/obo/VT_0000030"


