import asyncio
import csv
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from ethopipe.loader import (
    CSVLoader,
    FirestoreLoader,
    generate_observation_doc_id,
)
from ethopipe.models import EthologicalObservation, QuarantineRecord


def get_test_payload() -> dict:
    """Helper to return a valid dictionary matching EthologicalObservation."""
    return {
        "subject_id": "SUB-DOG-100",
        "timestamp": datetime.now(),
        "species": "Canis lupus familiaris",
        "location": "Behavioral Evaluation Lab B",
        "latitude": 42.3601,
        "longitude": -71.0589,
        "behavior_type": "yawning",
        "behavior_value": "2 yawn events",
        "severity_score": 2,
        "heart_rate": 90,
        "heart_rate_unit": "BPM",
        "body_temp": 38.2,
        "temp_unit": "°C",
        "respiratory_rate": 20,
        "respiratory_rate_unit": "breaths/min",
        "observation_method": "HumanObservation",
        "narrative": "Subject exhibited displacement yawning when stranger approached.",
    }


def test_deterministic_doc_id_generation():
    """Verify that generate_observation_doc_id produces consistent and deterministic SHA-256 hashes."""
    payload = get_test_payload()
    obs = EthologicalObservation(**payload)

    doc_id_1 = generate_observation_doc_id(obs)
    doc_id_2 = generate_observation_doc_id(obs)

    # Assert consistency
    assert doc_id_1 == doc_id_2
    assert len(doc_id_1) == 64  # SHA-256 hash length in hex

    # Verify that changing a parameter alters the hash
    obs.behavior_type = "panting"
    doc_id_3 = generate_observation_doc_id(obs)
    assert doc_id_1 != doc_id_3


def test_firestore_loader_single_load():
    """Verify that a single observation is correctly written to the mocked Firestore client."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()

    # Configure AsyncMock for asynchronous Firestore document set
    mock_document.set = AsyncMock()
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection

    loader = FirestoreLoader(collection_name="observations_test", client=mock_client)
    obs = EthologicalObservation(**get_test_payload())

    doc_id = asyncio.run(loader.load_observation(obs))
    expected_doc_id = generate_observation_doc_id(obs)

    assert doc_id == expected_doc_id
    mock_client.collection.assert_called_once_with("observations_test")
    mock_collection.document.assert_called_once_with(expected_doc_id)
    mock_document.set.assert_called_once_with(obs.model_dump())


def test_firestore_loader_batch_load():
    """Verify that a batch of observations is loaded atomically using Firestore WriteBatch."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_batch = MagicMock()

    # Configure mock AsyncBatch commit
    mock_batch.commit = AsyncMock()
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection
    mock_client.batch.return_value = mock_batch

    loader = FirestoreLoader(
        collection_name="observations_batch_test", client=mock_client
    )

    payload_1 = get_test_payload()
    payload_1["subject_id"] = "SUB-DOG-101"

    payload_2 = get_test_payload()
    payload_2["subject_id"] = "SUB-DOG-102"

    obs_list = [
        EthologicalObservation(**payload_1),
        EthologicalObservation(**payload_2),
    ]

    doc_ids = asyncio.run(loader.load_observations_batch(obs_list))
    expected_ids = [generate_observation_doc_id(o) for o in obs_list]

    assert doc_ids == expected_ids
    assert mock_client.collection.call_count == 2
    assert mock_batch.set.call_count == 2
    mock_batch.commit.assert_called_once()


def test_csv_loader_single_write(tmp_path):
    """Verify that CSVLoader writes a single observation, initializing headers correctly."""
    csv_file = tmp_path / "observations.csv"
    loader = CSVLoader(str(csv_file))
    obs = EthologicalObservation(**get_test_payload())

    doc_id = asyncio.run(loader.load_observation(obs))
    assert doc_id == generate_observation_doc_id(obs)
    assert csv_file.exists()

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["subject_id"] == "SUB-DOG-100"
        assert rows[0]["behavior_type"] == "yawning"
        assert float(rows[0]["body_temp"]) == 38.2
        assert int(rows[0]["heart_rate"]) == 90


def test_csv_loader_batch_append(tmp_path):
    """Verify that CSVLoader appends batches correctly without duplicate headers."""
    csv_file = tmp_path / "observations_batch.csv"
    loader = CSVLoader(str(csv_file))

    payload_1 = get_test_payload()
    payload_1["subject_id"] = "SUB-DOG-201"

    payload_2 = get_test_payload()
    payload_2["subject_id"] = "SUB-DOG-202"

    obs_list = [
        EthologicalObservation(**payload_1),
        EthologicalObservation(**payload_2),
    ]

    # Write initial batch
    doc_ids = asyncio.run(loader.load_observations_batch(obs_list))
    expected_ids = [generate_observation_doc_id(o) for o in obs_list]
    assert doc_ids == expected_ids

    # Append subsequent single observation
    payload_3 = get_test_payload()
    payload_3["subject_id"] = "SUB-DOG-203"
    obs_single = EthologicalObservation(**payload_3)

    asyncio.run(loader.load_observation(obs_single))

    with open(csv_file, mode="r", encoding="utf-8") as f:
        # Check standard headers write
        lines = f.readlines()
        # Should contain: 1 header line + 3 data lines = 4 total lines
        assert len(lines) == 4

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 3
        assert rows[0]["subject_id"] == "SUB-DOG-201"
        assert rows[1]["subject_id"] == "SUB-DOG-202"
        assert rows[2]["subject_id"] == "SUB-DOG-203"


def test_firestore_loader_missing_dependency():
    """Verify FirestoreLoader raises ModuleNotFoundError when firestore is not installed."""
    from ethopipe import loader

    # Backup the original firestore module reference
    orig_firestore = loader.firestore
    try:
        loader.firestore = None
        # Create loader with no pre-configured client
        loader_instance = FirestoreLoader(collection_name="test")
        with pytest.raises(ModuleNotFoundError) as exc_info:
            _ = loader_instance.client
        assert "google-cloud-firestore is required" in str(exc_info.value)
    finally:
        loader.firestore = orig_firestore


def test_firestore_loader_quarantine_batch_load():
    """Verify that a batch of quarantine records is loaded atomically using Firestore WriteBatch."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_batch = MagicMock()

    # Configure mock AsyncBatch commit
    mock_batch.commit = AsyncMock()
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection
    mock_client.batch.return_value = mock_batch

    loader = FirestoreLoader(
        collection_name="observations_test",
        quarantine_collection_name="quarantine_test",
        client=mock_client,
    )

    records = [
        QuarantineRecord(
            raw_payload={"DogID": "D1", "HR": "invalid"},
            errors=["heart_rate: Input should be a valid integer"],
            ingested_at=datetime.now(),
            original_index=1,
        ),
        QuarantineRecord(
            raw_payload={"DogID": "D2", "HR": "invalid2"},
            errors=["heart_rate: Input should be a valid integer"],
            ingested_at=datetime.now(),
            original_index=2,
        ),
    ]

    doc_ids = asyncio.run(loader.load_quarantine_batch(records))
    assert len(doc_ids) == 2
    assert mock_client.collection.call_count == 2
    mock_client.collection.assert_called_with("quarantine_test")
    assert mock_batch.set.call_count == 2
    mock_batch.commit.assert_called_once()


def test_csv_loader_quarantine_batch_load(tmp_path):
    """Verify that CSVLoader appends quarantine records correctly, serializing dict/list fields."""
    csv_file = tmp_path / "test.csv"
    loader = CSVLoader(str(csv_file))

    records = [
        QuarantineRecord(
            raw_payload={"DogID": "D1", "HR": "invalid"},
            errors=["heart_rate: Input should be a valid integer"],
            ingested_at=datetime.now(),
            original_index=1,
        ),
        QuarantineRecord(
            raw_payload={"DogID": "D2", "HR": "invalid2"},
            errors=["heart_rate: Input should be a valid integer"],
            ingested_at=datetime.now(),
            original_index=2,
        ),
    ]

    doc_ids = asyncio.run(loader.load_quarantine_batch(records))
    assert len(doc_ids) == 2

    quarantine_csv = tmp_path / "test_quarantine.csv"
    assert quarantine_csv.exists()

    import json

    with open(quarantine_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert json.loads(rows[0]["raw_payload"]) == {"DogID": "D1", "HR": "invalid"}
        assert json.loads(rows[0]["errors"]) == [
            "heart_rate: Input should be a valid integer"
        ]
        assert int(rows[0]["original_index"]) == 1
        assert int(rows[1]["original_index"]) == 2


def test_firestore_loader_batch_concurrency():
    """Verify that a batch of >500 observations is chunked and committed concurrently."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()

    # Mock collection and document
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection

    # Track batches created
    batches = []
    def make_batch():
        b = MagicMock()
        b.commit = AsyncMock()
        batches.append(b)
        return b
    mock_client.batch.side_effect = make_batch

    loader = FirestoreLoader(collection_name="concurrency_test", client=mock_client)

    # Generate 501 identical payload observations (using differing subject IDs)
    payload = get_test_payload()
    obs_list = []
    for idx in range(501):
        p = payload.copy()
        p["subject_id"] = f"SUB-DOG-{idx}"
        obs_list.append(EthologicalObservation(**p))

    doc_ids = asyncio.run(loader.load_observations_batch(obs_list))

    # Check that 2 batches were created and both committed
    assert len(batches) == 2
    assert batches[0].commit.call_count == 1
    assert batches[1].commit.call_count == 1
    assert len(doc_ids) == 501


def test_firestore_loader_retry_mechanism(monkeypatch):
    """Verify that the retry mechanism retries transient exceptions and succeeds if they resolve."""
    from google.api_core.exceptions import ServiceUnavailable

    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()

    # Simulate 2 ServiceUnavailable failures then 1 success
    mock_set = AsyncMock(side_effect=[
        ServiceUnavailable("Transient error"),
        ServiceUnavailable("Transient error"),
        "Success"
    ])
    mock_document.set = mock_set
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection

    # Reduce sleep time for fast testing
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())

    loader = FirestoreLoader(collection_name="retry_test", client=mock_client)
    obs = EthologicalObservation(**get_test_payload())

    doc_id = asyncio.run(loader.load_observation(obs))
    expected_doc_id = generate_observation_doc_id(obs)

    assert doc_id == expected_doc_id
    assert mock_set.call_count == 3


def test_firestore_loader_retry_failure(monkeypatch):
    """Verify that the retry mechanism eventually raises the exception if it persists."""
    from google.api_core.exceptions import ServiceUnavailable

    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_document = MagicMock()

    # Simulate continuous failures
    mock_set = AsyncMock(side_effect=ServiceUnavailable("Persistent transient error"))
    mock_document.set = mock_set
    mock_collection.document.return_value = mock_document
    mock_client.collection.return_value = mock_collection

    # Reduce sleep time for fast testing
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())

    loader = FirestoreLoader(collection_name="retry_test", client=mock_client)
    obs = EthologicalObservation(**get_test_payload())

    with pytest.raises(ServiceUnavailable):
        asyncio.run(loader.load_observation(obs))

    # Should have been called max_retries = 5 times
    assert mock_set.call_count == 5

