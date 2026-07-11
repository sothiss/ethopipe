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
