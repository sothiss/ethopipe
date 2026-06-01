"""EthoPipe: Extract, Transform, Load Pipeline for Applied Canine Ethology."""

from ethopipe.models import EthologicalObservation
from ethopipe.ingestion import load_csv, load_json

__all__ = ["EthologicalObservation", "load_csv", "load_json"]
