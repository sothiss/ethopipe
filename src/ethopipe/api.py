"""REST API Service Layer for EthoPipe."""

import json
import os
import tempfile
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from pydantic import ValidationError

from ethopipe.ingestion import _pre_process_row, load_csv, load_json
from ethopipe.loader import BaseLoader, CSVLoader, FirestoreLoader
from ethopipe.models import EthologicalObservation

app = FastAPI(
    title="EthoPipe REST API",
    description="Deterministic Extract-Transform-Load web interface for Applied Canine Ethology",
    version="1.0.0",
)


def get_loader() -> BaseLoader:
    """Dependency provider for the persistence loader.

    Decouples storage configuration from route logic and enables clean mocking.
    """
    loader_type = os.environ.get("ETL_LOADER_TYPE", "firestore").lower()
    if loader_type == "csv":
        csv_path = os.environ.get("ETL_CSV_PATH", "web_observations.csv")
        return CSVLoader(csv_path)
    return FirestoreLoader()


@app.post(
    "/validate",
    status_code=status.HTTP_200_OK,
    summary="Validate individual observation",
    description="Statelessly validates an individual raw observation and returns resolved Darwin Core terms.",
)
async def validate_observation(
    request: Request,
    mapping: Optional[str] = Query(None),
):
    """Parses a single raw JSON body, applies preprocessing, normalizes Title Case

    behaviors, and runs strict Pydantic model validation.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload must be a valid JSON object.",
        )

    column_mapping = {}
    if mapping:
        try:
            column_mapping = json.loads(mapping)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The 'mapping' query parameter must be valid JSON.",
            )

    # Convert mapping keys or preprocessing rules statelessly
    processed = _pre_process_row(data, column_mapping)

    try:
        observation = EthologicalObservation(**processed)
        return observation.model_dump()
    except ValidationError as e:
        errors = [
            f"{err['loc'][0] if err['loc'] else '__root__'}: {err['msg']}"
            for err in e.errors()
        ]
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors},
        )


@app.post(
    "/ingest/csv",
    status_code=status.HTTP_200_OK,
    summary="Ingest batch from CSV",
    description="Accepts a raw CSV text body, cleanses data, validation-checks each row, loads valid entries, and returns a quarantine log.",
)
async def ingest_csv(
    request: Request,
    mapping: Optional[str] = Query(None),
    loader: BaseLoader = Depends(get_loader),
):
    """Processes a raw CSV text body using the ingestion pipeline and persists

    valid records.
    """
    body = await request.body()
    csv_text = body.decode("utf-8")

    column_mapping = {}
    if mapping:
        try:
            column_mapping = json.loads(mapping)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The 'mapping' query parameter must be valid JSON.",
            )

    # Save CSV content to temporary file to leverage ingestion load_csv module safely
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv", encoding="utf-8"
    ) as tmp:
        tmp.write(csv_text)
        tmp_path = tmp.name

    try:
        valid_obs, quarantine = load_csv(tmp_path, column_mapping)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # Batch persist validated records
    loaded_ids = await loader.load_observations_batch(valid_obs)

    # Batch persist quarantine records
    quarantine_ids = await loader.load_quarantine_batch(quarantine)

    return {
        "status": "success" if not quarantine else "partial_success",
        "processed_count": len(valid_obs) + len(quarantine),
        "valid_count": len(valid_obs),
        "quarantine_count": len(quarantine),
        "loaded_ids": loaded_ids,
        "quarantine_ids": quarantine_ids,
        "quarantine": {str(q.original_index): q.errors for q in quarantine},
    }


@app.post(
    "/ingest/json",
    status_code=status.HTTP_200_OK,
    summary="Ingest batch from JSON list",
    description="Accepts a JSON list of raw observations, validates elements, loads valid entries, and returns a quarantine log.",
)
async def ingest_json(
    request: Request,
    mapping: Optional[str] = Query(None),
    loader: BaseLoader = Depends(get_loader),
):
    """Processes a raw JSON list body using the ingestion pipeline and persists

    valid records.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload must be a valid JSON list.",
        )

    if not isinstance(data, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The payload must be a JSON array (list).",
        )

    column_mapping = {}
    if mapping:
        try:
            column_mapping = json.loads(mapping)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The 'mapping' query parameter must be valid JSON.",
            )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name

    try:
        valid_obs, quarantine = load_json(tmp_path, column_mapping)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # Batch persist validated records
    loaded_ids = await loader.load_observations_batch(valid_obs)

    # Batch persist quarantine records
    quarantine_ids = await loader.load_quarantine_batch(quarantine)

    return {
        "status": "success" if not quarantine else "partial_success",
        "processed_count": len(valid_obs) + len(quarantine),
        "valid_count": len(valid_obs),
        "quarantine_count": len(quarantine),
        "loaded_ids": loaded_ids,
        "quarantine_ids": quarantine_ids,
        "quarantine": {str(q.original_index): q.errors for q in quarantine},
    }
