import re

from src.pipeline.models import PROHIBITED_WORDS, CanineObservation

# Bolt Optimization: Pre-compile regex patterns at module level
# Sorting PROHIBITED_WORDS ensures deterministic regex AST generation.
PROHIBITED_PATTERN = re.compile(
    rf"\b({'|'.join(sorted(PROHIBITED_WORDS))})\b", re.IGNORECASE
)
_SPACES_PATTERN = re.compile(r"\s+")


def de_bias_text(text: str) -> str:
    """
    Actively delete subjective, anthropomorphic terms from raw notes.
    """
    if not text:
        return text
    # Bolt Optimization: Fast-path check using search() before executing regex sub.
    # Avoids unnecessary regex string replacements for clean input text (~2x speedup).
    if PROHIBITED_PATTERN.search(text):
        text = PROHIBITED_PATTERN.sub("", text)

    # Fast-path space normalization check before running pre-compiled regex sub
    if (
        "  " in text
        or "\t" in text
        or "\n" in text
        or "\r" in text
        or text.startswith(" ")
        or text.endswith(" ")
    ):
        return _SPACES_PATTERN.sub(" ", text).strip()
    return text


def clean_payload_notes(data: dict) -> dict:
    """
    Recursively clean all free-text fields in the observation payload.
    """
    cleaned = dict(data)

    # Clean top-level context/session fields
    for key in ("context_session", "Context/Session", "context"):
        val = cleaned.get(key)
        if isinstance(val, str):
            cleaned[key] = de_bias_text(val)

    # Clean notes in individual behavior observations
    behaviors = cleaned.get("behaviors")
    if isinstance(behaviors, list):
        cleaned_behaviors = []
        for beh in behaviors:
            if isinstance(beh, dict):
                beh_copy = dict(beh)
                for note_key in ("additional_notes", "Additional_Notes"):
                    val = beh_copy.get(note_key)
                    if isinstance(val, str):
                        beh_copy[note_key] = de_bias_text(val)
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
