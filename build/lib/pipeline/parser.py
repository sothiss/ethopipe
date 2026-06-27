from .models import EthologicalIncident


def normalize_incident(data: dict) -> EthologicalIncident:
    """
    Validate and normalize an incoming incident payload.
    """
    return EthologicalIncident(**data)
