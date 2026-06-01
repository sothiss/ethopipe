"""Loader Module for EthoPipe to persist validated ethological observations."""

import asyncio
import csv
import hashlib
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Optional

from ethopipe.models import EthologicalObservation, QuarantineRecord

try:
    from google.cloud import firestore
    from google.cloud.firestore import AsyncClient as FirestoreAsyncClient
except ModuleNotFoundError:  # pragma: no cover
    firestore = None
    FirestoreAsyncClient = Any

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

    @abstractmethod
    async def load_quarantine_batch(self, quarantine_records: list[QuarantineRecord]) -> list[str]:
        """Persists a batch of quarantine records.

        Args:
            quarantine_records: List of QuarantineRecord objects.

        Returns:
            list[str]: List of successfully committed record/document IDs.
        """
        pass



class FirestoreLoader(BaseLoader):
    """Asynchronous loader to persist validated observations to Google Cloud Firestore."""

    def __init__(
        self,
        collection_name: str = "observations",
        quarantine_collection_name: str = "quarantine",
        client: Optional[FirestoreAsyncClient] = None,
    ):
        """Initializes the FirestoreLoader.

        Args:
            collection_name: Target Firestore collection. Defaults to "observations".
            quarantine_collection_name: Target Firestore collection for quarantined data. Defaults to "quarantine".
            client: Optional pre-configured FirestoreAsyncClient. If None,
              auto-initializes.
        """
        self.collection_name = collection_name
        self.quarantine_collection_name = quarantine_collection_name
        self._client = client

    @property
    def client(self) -> FirestoreAsyncClient:
        """Lazy-loaded Firestore AsyncClient.

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

    async def load_quarantine_batch(self, quarantine_records: list[QuarantineRecord]) -> list[str]:
        """Persists a batch of quarantine records atomically using Firestore WriteBatch.

        Accommodates Firestore's maximum limits of 500 writes per batch by automatically
        chunking larger datasets.

        Args:
            quarantine_records: List of QuarantineRecord objects.

        Returns:
            list[str]: List of successfully committed deterministic document IDs.
        """
        if not quarantine_records:
            return []

        doc_ids = []
        batch = self.client.batch()
        batch_counter = 0
        committed_ids = []

        for rec in quarantine_records:
            timestamp_str = rec.ingested_at.isoformat()
            raw_payload_str = json.dumps(rec.raw_payload, sort_keys=True)
            raw_key = f"{raw_payload_str}_{timestamp_str}_{rec.original_index}"
            doc_id = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

            doc_ref = self.client.collection(self.quarantine_collection_name).document(doc_id)
            batch.set(doc_ref, rec.model_dump())
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

        logger.info(f"Successfully loaded batch of {len(committed_ids)} quarantine records to Firestore.")
        return committed_ids


class CSVLoader(BaseLoader):
    """Loader to export and append validated observations to a local CSV file."""

    def __init__(self, file_path: str, quarantine_file_path: Optional[str] = None):
        """Initializes the CSVLoader.

        Args:
            file_path: Absolute or relative path to the target CSV file.
            quarantine_file_path: Optional path to the CSV file for quarantined data.
        """
        self.file_path = file_path
        if quarantine_file_path is None:
            if file_path.endswith(".csv"):
                self.quarantine_file_path = file_path[:-4] + "_quarantine.csv"
            else:
                self.quarantine_file_path = file_path + "_quarantine"
        else:
            self.quarantine_file_path = quarantine_file_path

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

    def _write_quarantine_batch_sync(self, quarantine_records: list[QuarantineRecord], mode: str = "a") -> list[str]:
        """Synchronous implementation to write a batch of quarantine records to the CSV."""
        if not quarantine_records:
            return []

        file_exists = os.path.exists(self.quarantine_file_path) and os.path.getsize(self.quarantine_file_path) > 0
        
        data_dicts = []
        for rec in quarantine_records:
            data = rec.model_dump()
            # Serialize dict/list fields as JSON strings for CSV storage
            data["raw_payload"] = json.dumps(data["raw_payload"])
            data["errors"] = json.dumps(data["errors"])
            data_dicts.append(data)

        headers = list(data_dicts[0].keys())
        write_header = not file_exists or mode == "w"

        with open(self.quarantine_file_path, mode=mode, encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerows(data_dicts)

        # Generate deterministic IDs for the quarantine records
        doc_ids = []
        for rec in quarantine_records:
            timestamp_str = rec.ingested_at.isoformat()
            raw_payload_str = json.dumps(rec.raw_payload, sort_keys=True)
            raw_key = f"{raw_payload_str}_{timestamp_str}_{rec.original_index}"
            doc_ids.append(hashlib.sha256(raw_key.encode("utf-8")).hexdigest())
        return doc_ids

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

    async def load_quarantine_batch(self, quarantine_records: list[QuarantineRecord]) -> list[str]:
        """Asynchronously writes/appends a batch of quarantine records to the CSV.

        Offloads blocking file system I/O to a background thread.
        """
        return await asyncio.to_thread(self._write_quarantine_batch_sync, quarantine_records, "a")

