"""Rule-Based Narrative Extractor for EthoPipe to parse unstructured reports."""

import hashlib
import logging
import re
from datetime import datetime
from typing import Any, Optional, Union

from ethopipe.models import EthologicalObservation

logger = logging.getLogger("ethopipe.extraction")

# Pre-compiled regular expressions for physiological vitals and severity scores
HR_RE = re.compile(
    r"(?i)(?:heart\s*rate|hr)(?:\s*(?:recorded\s*at|is|of|:)?\s*)(\d+)\s*(?:bpm)?\b|\b(\d+)\s*(?:bpm)\b"
)
TEMP_RE = re.compile(
    r"(?i)(?:temp(?:erature)?)(?:\s*(?:was|is|recorded\s*at|:)?\s*)(\d+(?:\.\d+)?)\s*(?:°?\s*c)\b|\b(\d+(?:\.\d+)?)\s*(?:°?\s*c)\b"
)
RESP_RE = re.compile(
    r"(?i)(?:respiratory\s*rate|resp\s*rate|rr)(?:\s*(?:was|is|recorded\s*at|:)?\s*)(\d+)\s*(?:breaths/min|breaths\s*/\s*min)?\b|\b(\d+)\s*(?:breaths/min|breaths\s*/\s*min)\b"
)
CORTISOL_RE = re.compile(
    r"(?i)(?:cortisol)(?:\s*(?:level|concentration)?)(?:\s*(?:was|is|recorded\s*at|of|:)?\s*)(\d+(?:\.\d+)?)\s*(?:ng/mL|ng/ml)?\b|\b(\d+(?:\.\d+)?)\s*(?:ng/mL|ng/ml)\b"
)
SEVERITY_RE = re.compile(
    r"(?i)(?:severity(?:\s*score)?)(?:\s*(?:was|is|of|:)?\s*)([1-5])\b"
)

# Set of biological matrices for cortisol assay scanning
MATRICES = ["saliva", "hair", "blood", "serum", "plasma", "urine", "feces", "claws"]

# Stemmed behavior regular expression rules with surrounding count matches
BEHAVIOR_RULES = {
    "growling": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+growl(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\bgrowl(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bgrowl(?:s|ed|ing)?\b")
    ],
    "whining": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+whin(?:e|es|ed|ing)?\b"),
        re.compile(r"(?i)\bwhin(?:e|es|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bwhin(?:e|es|ed|ing)?\b")
    ],
    "panting": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+pant(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\bpant(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bpant(?:s|ed|ing)?\b")
    ],
    "yawning": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+yawn(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\byawn(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\byawn(?:s|ed|ing)?\b")
    ],
    "avoidance": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+avoid(?:s|ed|ing|ance)?\b"),
        re.compile(r"(?i)\bavoid(?:s|ed|ing|ance)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bavoid(?:s|ed|ing|ance)?\b")
    ],
    "barks": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+bark(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\bbark(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bbark(?:s|ed|ing)?\b")
    ],
    "lunges": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+lung(?:e|es|ed|ing)?\b"),
        re.compile(r"(?i)\blung(?:e|es|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\blung(?:e|es|ed|ing)?\b")
    ],
    "cowers": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+cower(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\bcower(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bcower(?:s|ed|ing)?\b")
    ],
    "play_bow": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+play\s*bow(?:s|ed|ing)?\b"),
        re.compile(r"(?i)\bplay\s*bow(?:s|ed|ing)?\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\bplay\s*bow(?:s|ed|ing)?\b")
    ],
    "licking_of_lips": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+(?:lic(?:k|ks|ked|king)?\s*(?:of\s*)?lips?|lip\s*lic(?:k|ks|ked|king)?)\b"),
        re.compile(r"(?i)\b(?:lic(?:k|ks|ked|king)?\s*(?:of\s*)?lips?|lip\s*lic(?:k|ks|ked|king)?)\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\b(?:lic(?:k|ks|ked|king)?\s*(?:of\s*)?lips?|lip\s*lic(?:k|ks|ked|king)?)\b")
    ],
    "looking_away": [
        re.compile(r"(?i)\b(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\s+(?:loo(?:k|ks|ked|king)?\s*away)\b"),
        re.compile(r"(?i)\b(?:loo(?:k|ks|ked|king)?\s*away)\s+(\d+|once|twice|thrice|one|two|three|four|five|continuous(?:ly)?)\b"),
        re.compile(r"(?i)\b(?:loo(?:k|ks|ked|king)?\s*away)\b")
    ]
}


def _resolve_frequency_value(raw_val: Optional[str]) -> Union[int, str]:
    """Translates numeric digits and spelled-out English frequency terms to integer values."""
    if not raw_val:
        return 1

    clean_val = raw_val.strip().lower()
    word_map = {
        "once": 1,
        "one": 1,
        "twice": 2,
        "two": 2,
        "thrice": 3,
        "three": 3,
        "four": 4,
        "five": 5,
        "continuous": "continuous",
        "continuously": "continuous"
    }

    if clean_val in word_map:
        return word_map[clean_val]

    try:
        return int(clean_val)
    except ValueError:
        return clean_val


def extract_from_narrative(
    narrative: str,
    subject_id: str,
    timestamp: datetime,
    location: str,
    dog_size_category: Optional[str] = None,
    observation_method: str = "HumanObservation",
) -> list[EthologicalObservation]:
    """Statelessly parses unstructured reports and extracts validated

    EthologicalObservation instances.

    Args:
        narrative: Unstructured clinical text report.
        subject_id: Unique individual ID for the subject.
        timestamp: Temporal metadata.
        location: Spatial locality string.
        dog_size_category: Optional size category for heart rate validation bounds.
        observation_method: basisOfRecord mapping ("HumanObservation").

    Returns:
        list[EthologicalObservation]: A list of validated observation models containing
        all resolved behaviors, frequency values, and extracted physiological vitals.
    """
    if not narrative:
        return []

    # 1. Parse Vitals & Biomarkers
    heart_rate = None
    hr_match = HR_RE.search(narrative)
    if hr_match:
        # Match groups can fall under group 1 or 2 due to alternative patterns
        hr_str = hr_match.group(1) or hr_match.group(2)
        if hr_str:
            heart_rate = int(hr_str)

    body_temp = None
    temp_match = TEMP_RE.search(narrative)
    if temp_match:
        temp_str = temp_match.group(1) or temp_match.group(2)
        if temp_str:
            body_temp = float(temp_str)

    respiratory_rate = None
    resp_match = RESP_RE.search(narrative)
    if resp_match:
        resp_str = resp_match.group(1) or resp_match.group(2)
        if resp_str:
            respiratory_rate = int(resp_str)

    cortisol_level = None
    cortisol_match = CORTISOL_RE.search(narrative)
    if cortisol_match:
        cort_str = cortisol_match.group(1) or cortisol_match.group(2)
        if cort_str:
            cortisol_level = float(cort_str)

    # Scans for cortisol matrix assay
    cortisol_matrix = None
    for m in MATRICES:
        if re.search(rf"(?i)\b{m}\b", narrative):
            cortisol_matrix = m
            break

    severity_score = None
    severity_match = SEVERITY_RE.search(narrative)
    if severity_match:
        sev_str = severity_match.group(1)
        if sev_str:
            severity_score = int(sev_str)

    # 2. Extract Behaviors
    extracted_behaviors = {}

    for canonical_name, regex_list in BEHAVIOR_RULES.items():
        matched = False
        value = 1

        for regex in regex_list:
            match = regex.search(narrative)
            if match:
                matched = True
                # If the regex matched with a prefix/suffix capture group
                if len(match.groups()) > 0 and match.group(1):
                    value = _resolve_frequency_value(match.group(1))
                else:
                    value = 1
                break

        if matched:
            extracted_behaviors[canonical_name] = value

    # 3. Fallback to Neutral post if no behavioral metrics are found but vitals exist
    if not extracted_behaviors and (
        heart_rate is not None or body_temp is not None or respiratory_rate is not None
    ):
        extracted_behaviors["neutral"] = 1

    # 4. Construct EthologicalObservation instances
    observations = []

    for behavior_type, behavior_value in extracted_behaviors.items():
        payload = {
            "subject_id": subject_id,
            "timestamp": timestamp,
            "location": location,
            "dog_size_category": dog_size_category,
            "behavior_type": behavior_type,
            "behavior_value": behavior_value,
            "severity_score": severity_score,
            "heart_rate": heart_rate,
            "heart_rate_unit": "BPM",
            "body_temp": body_temp,
            "temp_unit": "°C",
            "respiratory_rate": respiratory_rate,
            "respiratory_rate_unit": "breaths/min",
            "observation_method": observation_method,
            "narrative": narrative,
        }

        # Conditionally add cortisol if extracted
        if cortisol_level is not None:
            payload["cortisol_level"] = cortisol_level
            payload["cortisol_unit"] = "ng/mL"
            payload["cortisol_matrix"] = cortisol_matrix

        try:
            obs = EthologicalObservation(**payload)
            observations.append(obs)
        except ValidationError as e:
            logger.warning(
                f"Failed to validate extracted observation for {behavior_type}: {e}"
            )

    return observations
