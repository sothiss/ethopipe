"""Google Cloud Platform Integration Module for EthoPipe.

Handles GCS data ingestion and Vertex AI structured ethological behavioral extraction.
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Any, Optional, Union, List

import httpx
import google.auth
import google.auth.transport.requests
from google.cloud import storage

from ethopipe.models import (
    EthologicalObservation,
    BehavioralObservation,
    EthogramExtractionLog,
)
from ethopipe.extraction import (
    HR_RE,
    TEMP_RE,
    RESP_RE,
    CORTISOL_RE,
    SEVERITY_RE,
    MATRICES,
    _resolve_frequency_value,
)

logger = logging.getLogger("ethopipe.gcp")


def download_gcs_file(bucket_name: str, blob_name: str) -> str:
    """Downloads a file's contents from Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        blob_name: The path/name of the blob within the bucket.

    Returns:
        str: The decoded file content.
    """
    logger.info(f"Downloading blob '{blob_name}' from bucket '{bucket_name}'")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text(encoding="utf-8")
    return content


def _to_vertex_schema(schema: dict) -> dict:
    """Recursively converts a standard JSON schema into the format expected by Vertex AI.

    Vertex AI schema requirements:
    - Uppercase types (e.g. 'OBJECT', 'ARRAY', 'STRING', 'NUMBER', 'INTEGER')
    - No unsupported keys (like '$ref', '$schema')
    """
    vertex_schema = {}
    
    if "type" in schema:
        t = schema["type"]
        if isinstance(t, str):
            vertex_schema["type"] = t.upper()
        else:
            vertex_schema["type"] = t

    if "properties" in schema:
        vertex_schema["properties"] = {
            k: _to_vertex_schema(v) for k, v in schema["properties"].items()
        }

    if "items" in schema:
        vertex_schema["items"] = _to_vertex_schema(schema["items"])

    if "required" in schema:
        vertex_schema["required"] = schema["required"]

    if "enum" in schema:
        vertex_schema["enum"] = schema["enum"]

    if "description" in schema:
        vertex_schema["description"] = schema["description"]

    return vertex_schema


async def call_vertex_ai_for_extraction(
    narrative: str,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    model_id: str = "gemini-1.5-flash",
) -> EthogramExtractionLog:
    """Calls the Vertex AI Gemini REST API endpoint to extract structured behavior observations.

    Args:
        narrative: Unstructured handler notes or clinical report text.
        project_id: Google Cloud Project ID. Auto-detected via ADC if None.
        location: Target Google Cloud Region/Location. Defaults to "us-central1".
        model_id: Target Gemini model ID. Defaults to "gemini-1.5-flash".

    Returns:
        EthogramExtractionLog: Structured extraction results matching Pydantic model.
    """
    # 1. Retrieve Active Application Default Credentials (ADC)
    credentials, credentials_project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    # Resolve Project ID
    resolved_project = (
        project_id
        or credentials_project_id
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("GCP_PROJECT")
        or "gen-lang-client-0629166560"
    )

    # Refresh credentials to obtain access token
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    token = credentials.token

    if not token:
        raise RuntimeError("Failed to obtain GCP authentication token.")

    # 2. Build Vertex AI REST Endpoint URL
    url = (
        f"https://{location}-aiplatform.googleapis.com/v1/"
        f"projects/{resolved_project}/locations/{location}/"
        f"publishers/google/models/{model_id}:generateContent"
    )

    # 3. Generate structured schema for the Pydantic model
    pydantic_schema = EthogramExtractionLog.model_json_schema()
    vertex_schema = _to_vertex_schema(pydantic_schema)

    # 4. Construct Prompt
    prompt_text = (
        "Analyze the following unstructured canine behavior handler notes.\n"
        "Extract all occurrences of standard canine behaviors and map them to their canonical identifiers, "
        "ontology URIs, the exact source text, and a confidence score.\n\n"
        "Do not extract general states that do not match the canonical behavior list.\n\n"
        f"Handler Notes:\n{narrative}"
    )

    # 5. Build POST Body
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_text}],
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": vertex_schema,
            "temperature": 0.0,  # Enforce determinism
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # 6. Execute Async POST request to Vertex AI REST API
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"Vertex AI API call failed: {response.status_code} - {response.text}")
            raise httpx.HTTPStatusError(
                f"Vertex AI returned status {response.status_code}: {response.text}",
                request=response.request,
                response=response,
            )

        response_data = response.json()

    # 7. Parse output content candidates
    try:
        candidate = response_data["candidates"][0]
        text_content = candidate["content"]["parts"][0]["text"]
        structured_data = json.loads(text_content)
        return EthogramExtractionLog(**structured_data)
    except (KeyError, IndexError, ValueError, TypeError) as e:
        logger.error(f"Failed to parse response payload from Vertex AI: {e}. Raw response: {response_data}")
        raise ValueError(f"Invalid response structure from Vertex AI: {str(e)}")


def extract_vitals_from_text(narrative: str) -> dict[str, Any]:
    """Helper using regexes from extraction.py to parse physiological vitals from notes."""
    vitals = {}

    # Heart Rate
    hr_match = HR_RE.search(narrative)
    if hr_match:
        hr_str = hr_match.group(1) or hr_match.group(2)
        if hr_str:
            vitals["heart_rate"] = int(hr_str)

    # Body Temp
    temp_match = TEMP_RE.search(narrative)
    if temp_match:
        temp_str = temp_match.group(1) or temp_match.group(2)
        if temp_str:
            vitals["body_temp"] = float(temp_str)

    # Respiratory Rate
    resp_match = RESP_RE.search(narrative)
    if resp_match:
        resp_str = resp_match.group(1) or resp_match.group(2)
        if resp_str:
            vitals["respiratory_rate"] = int(resp_str)

    # Cortisol
    cortisol_match = CORTISOL_RE.search(narrative)
    if cortisol_match:
        cort_str = cortisol_match.group(1) or cortisol_match.group(2)
        if cort_str:
            vitals["cortisol_level"] = float(cort_str)

    # Cortisol Matrix
    for m in MATRICES:
        if re.search(rf"(?i)\b{m}\b", narrative):
            vitals["cortisol_matrix"] = m
            break

    # Severity Score
    severity_match = SEVERITY_RE.search(narrative)
    if severity_match:
        sev_str = severity_match.group(1)
        if sev_str:
            vitals["severity_score"] = int(sev_str)

    return vitals


async def process_narrative_with_gcp(
    narrative: str,
    subject_id: str,
    timestamp: datetime,
    location: str,
    dog_size_category: Optional[str] = None,
    observation_method: str = "HumanObservation",
    project_id: Optional[str] = None,
    location_gcp: str = "us-central1",
) -> list[EthologicalObservation]:
    """Orchestrates the hybrid regex-vitals and Vertex AI behavioral extraction pipeline.

    Args:
        narrative: Raw text description of the observation event.
        subject_id: Dog ID (dwc:individualID).
        timestamp: Time of observation (dwc:eventDate).
        location: Geographic locality (dwc:locality).
        dog_size_category: Size category for heart rate validation bounds.
        observation_method: Record basis method (dwc:basisOfRecord).
        project_id: Optional GCP Project ID.
        location_gcp: Google Cloud Region location.

    Returns:
        list[EthologicalObservation]: Validated models ready for loading.
    """
    # 1. Parse vitals locally using high-performance, deterministic regex rules
    vitals = extract_vitals_from_text(narrative)

    # 2. Extract behaviors using the Vertex AI semantic intelligence layer
    try:
        extraction_log = await call_vertex_ai_for_extraction(
            narrative=narrative,
            project_id=project_id,
            location=location_gcp,
        )
    except Exception as e:
        logger.warning(f"Vertex AI behavior extraction failed, falling back to local regex-only extraction: {e}")
        # Import local extractor fallback to prevent pipeline failure
        from ethopipe.extraction import extract_from_narrative
        return extract_from_narrative(
            narrative=narrative,
            subject_id=subject_id,
            timestamp=timestamp,
            location=location,
            dog_size_category=dog_size_category,
            observation_method=observation_method,
        )

    observations = []

    # 3. Transform each extracted BehavioralObservation to the standard EthologicalObservation
    for item in extraction_log.observations:
        # Resolve frequency value if possible by scanning the local source text snippet
        # If no numeric/spelled-out count matches, default behavior_value to 1 occurrence
        behavior_value: Union[int, str] = 1
        words = item.source_text.split()
        for w in words:
            resolved = _resolve_frequency_value(w)
            if isinstance(resolved, int) or resolved == "continuous":
                behavior_value = resolved
                break

        # Construct payload merged with vitals
        payload = {
            "subject_id": subject_id,
            "timestamp": timestamp,
            "location": location,
            "dog_size_category": dog_size_category,
            "behavior_type": item.behavior.value,
            "behavior_value": behavior_value,
            "severity_score": vitals.get("severity_score"),
            "heart_rate": vitals.get("heart_rate"),
            "heart_rate_unit": "BPM",
            "body_temp": vitals.get("body_temp"),
            "temp_unit": "°C",
            "respiratory_rate": vitals.get("respiratory_rate"),
            "respiratory_rate_unit": "breaths/min",
            "observation_method": observation_method,
            "narrative": narrative,
            "behavior_type_id": item.ontology_uri,
        }

        if "cortisol_level" in vitals:
            payload["cortisol_level"] = vitals["cortisol_level"]
            payload["cortisol_unit"] = "ng/mL"
            payload["cortisol_matrix"] = vitals.get("cortisol_matrix")

        try:
            obs = EthologicalObservation(**payload)
            observations.append(obs)
        except Exception as ve:
            logger.warning(f"Failed to validate observation model for behavior '{item.behavior.value}': {ve}")

    # Fallback to a neutral observation if no behaviors were found but vitals exist
    if not observations and (
        vitals.get("heart_rate") is not None
        or vitals.get("body_temp") is not None
        or vitals.get("respiratory_rate") is not None
    ):
        payload = {
            "subject_id": subject_id,
            "timestamp": timestamp,
            "location": location,
            "dog_size_category": dog_size_category,
            "behavior_type": "neutral",
            "behavior_value": 1,
            "severity_score": vitals.get("severity_score"),
            "heart_rate": vitals.get("heart_rate"),
            "heart_rate_unit": "BPM",
            "body_temp": vitals.get("body_temp"),
            "temp_unit": "°C",
            "respiratory_rate": vitals.get("respiratory_rate"),
            "respiratory_rate_unit": "breaths/min",
            "observation_method": observation_method,
            "narrative": narrative,
            "behavior_type_id": "http://purl.obolibrary.org/obo/NBO_0000311",
        }
        if "cortisol_level" in vitals:
            payload["cortisol_level"] = vitals["cortisol_level"]
            payload["cortisol_unit"] = "ng/mL"
            payload["cortisol_matrix"] = vitals.get("cortisol_matrix")
        try:
            obs = EthologicalObservation(**payload)
            observations.append(obs)
        except Exception as ve:
            logger.warning(f"Failed to validate fallback neutral observation model: {ve}")

    return observations
