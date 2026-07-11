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
