"""Loader Module for EthoPipe to persist validated ethological observations."""

import asyncio
import csv
import hashlib
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING

from ethopipe.models import EthologicalObservation

if TYPE_CHECKING:
    from google.cloud.firestore import AsyncClient as FirestoreAsyncClient
else:
    FirestoreAsyncClient = Any

try:
    from google.cloud import firestore
except ModuleNotFoundError:  # pragma: no cover
    firestore = None

logger = logging.getLogger("ethopipe.loader")


def generate_observation_doc_id(obs: EthologicalObservation) -> str:
    """Generates a unique, deterministic SHA-256 document ID to guarantee

    idempotency and scientific reproducibility.
    """
    timestamp_str = obs.timestamp.isoformat()
    raw_key = f"{obs.subject_id}_{timestamp_str}_{obs.behavior_type}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


class BaseLoader(ABC):
    """Abstract Base Class defining the standard interface for EthoPipe Loaders."""

    @abstractmethod
    async def load_observation(self, observation: EthologicalObservation) -> str:
        """Loads a single validated observation.

        Args:
            observation: The validated EthologicalObservation record.

        Returns:
            str: The identifier of the loaded document or record.
        """
        pass

    @abstractmethod
    async def load_observations_batch(self, observations: list[EthologicalObservation]) -> list[str]:
        """Loads a batch of validated observations.

        Args:
            observations: List of validated EthologicalObservation records.

        Returns:
            list[str]: The list of loaded record identifiers.
        """
        pass


class FirestoreLoader(BaseLoader):
    """Asynchronous loader to persist validated observations to Google Cloud Firestore."""

    def __init__(
        self,
        collection_name: str = "observations",
        client: Optional[FirestoreAsyncClient] = None,
    ):
        """Initializes the FirestoreLoader.

        Args:
            collection_name: Target Firestore collection. Defaults to "observations".
            client: Optional pre-configured firestore.AsyncClient. If None,
              auto-initializes.
        """
        self.collection_name = collection_name
        self._client = client

    @property
    def client(self) -> FirestoreAsyncClient:
        """Lazy-loaded firestore.AsyncClient.

        Automatically detects FIRESTORE_EMULATOR_HOST environment variable to support
        safe, local development and regression testing.
        """
        if self._client is None:
            if firestore is None:
                raise ModuleNotFoundError(
                    "google-cloud-firestore is required for FirestoreLoader. "
                    "Install it with `pip install google-cloud-firestore`."
                )
            # Check for emulator settings to allow offline/local testing
            emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")
            if emulator_host:
                logger.info(f"Connecting to local Firestore emulator at {emulator_host}")
            self._client = firestore.AsyncClient()
        return self._client

    async def load_observation(self, observation: EthologicalObservation) -> str:
        """Persists a single validated observation into Firestore.

        Uses a deterministic document ID to prevent duplicate ingestion events.

        Args:
            observation: Validated EthologicalObservation.

        Returns:
            str: The deterministic Firestore document ID.
        """
        doc_id = generate_observation_doc_id(observation)
        doc_ref = self.client.collection(self.collection_name).document(doc_id)
        
        # model_dump() converts datetime fields to native Pydantic structures.
        # Firestore handles datetime, float, int, and string types natively.
        data = observation.model_dump()
        await doc_ref.set(data)
        logger.debug(f"Successfully loaded observation {doc_id} to Firestore.")
        return doc_id

    async def load_observations_batch(self, observations: list[EthologicalObservation]) -> list[str]:
        """Persists a batch of observations atomically using Firestore WriteBatch.

        Accommodates Firestore's maximum limits of 500 writes per batch by automatically
        chunking larger datasets.

        Args:
            observations: List of validated EthologicalObservation objects.

        Returns:
            list[str]: List of successfully committed deterministic document IDs.
        """
        if not observations:
            return []

        doc_ids = []
        batch = self.client.batch()
        batch_counter = 0
        committed_ids = []

        for obs in observations:
            doc_id = generate_observation_doc_id(obs)
            doc_ref = self.client.collection(self.collection_name).document(doc_id)
            batch.set(doc_ref, obs.model_dump())
            doc_ids.append(doc_id)
            batch_counter += 1

            if batch_counter == 500:
                await batch.commit()
                committed_ids.extend(doc_ids[-batch_counter:])
                batch = self.client.batch()
                batch_counter = 0

        if batch_counter > 0:
            await batch.commit()
            committed_ids.extend(doc_ids[-batch_counter:])

        logger.info(f"Successfully loaded batch of {len(committed_ids)} observations to Firestore.")
        return committed_ids


class CSVLoader(BaseLoader):
    """Loader to export and append validated observations to a local CSV file."""

    def __init__(self, file_path: str):
        """Initializes the CSVLoader.

        Args:
            file_path: Absolute or relative path to the target CSV file.
        """
        self.file_path = file_path

    def _write_observation_sync(self, observation: EthologicalObservation, mode: str = "a") -> str:
        """Synchronous implementation to append or write an observation to the CSV.

        Automatically initializes headers if the file does not exist.
        """
        file_exists = os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0
        data = observation.model_dump()
        headers = list(data.keys())

        # If writing in 'w' mode, force header write
        write_header = not file_exists or mode == "w"

        with open(self.file_path, mode=mode, encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerow(data)

        return generate_observation_doc_id(observation)

    def _write_batch_sync(self, observations: list[EthologicalObservation], mode: str = "a") -> list[str]:
        """Synchronous implementation to write a batch of observations to the CSV."""
        if not observations:
            return []

        file_exists = os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0
        data_dicts = [obs.model_dump() for obs in observations]
        headers = list(data_dicts[0].keys())

        write_header = not file_exists or mode == "w"

        with open(self.file_path, mode=mode, encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerows(data_dicts)

        return [generate_observation_doc_id(obs) for obs in observations]

    async def load_observation(self, observation: EthologicalObservation) -> str:
        """Asynchronously writes/appends a single observation to the CSV.

        Offloads blocking file system I/O to a background thread.
        """
        return await asyncio.to_thread(self._write_observation_sync, observation, "a")

    async def load_observations_batch(self, observations: list[EthologicalObservation]) -> list[str]:
        """Asynchronously writes/appends a batch of observations to the CSV.

        Offloads blocking file system I/O to a background thread.
        """
        return await asyncio.to_thread(self._write_batch_sync, observations, "a")
