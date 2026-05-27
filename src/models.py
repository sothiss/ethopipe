from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, Union
from datetime import datetime

class EthologicalObservation(BaseModel):
    model_config = ConfigDict(strict=True)

    # 1. Subject, Taxonomic, and Temporal Identification (Darwin Core Mapped)
    subject_id: str = Field(
        ..., 
        description="Maps to dwc:individualID. Unique identifier for the individual canine subject [5-8]."
    )
    timestamp: datetime = Field(
        ..., 
        description="Maps to dwc:eventDate. Date and time of observation in ISO 8601 format [5-8]."
    )
    species: Literal["Canis lupus familiaris"] = Field(
        "Canis lupus familiaris", 
        description="Maps to dwc:scientificName. Fixed to the domestic dog [5-8]."
    )

    # 2. Spatial Metadata (Darwin Core Mapped)
    location: str = Field(
        ..., 
        description="Maps to dwc:locality. Textual description of the observation location [5-8]."
    )
    latitude: Optional[float] = Field(
        None, 
        description="Maps to dwc:decimalLatitude in decimal degrees [5-8]."
    )
    longitude: Optional[float] = Field(
        None, 
        description="Maps to dwc:decimalLongitude in decimal degrees [5-7, 9]."
    )

    # 3. Behavioral Measurements (Operational Definitions)
    behavior_type: Literal[
        "barks", "lunges", "cowers", "stress_markers", "neutral", "play_bow", "licking_of_lips", "looking_away"
    ] = Field(
        ..., 
        description="Maps to dwc:measurementType. Categorical motor patterns grouped by stress, appeasement, and physiological reactivity [10-15]."
    )
    behavior_value: Union[int, float, str] = Field(
        ..., 
        description="Maps to dwc:measurementValue. Quantitative or categorical behavior data, such as frequency counts or durations [5-7, 9]."
    )
    severity_score: Optional[int] = Field(
        None, 
        ge=1, le=5, 
        description="A standardized intensity scale mapping minor displacement cues (1) to overt physiological or behavioral reactivity (5) [14, 15]."
    )

    # 4. Physiological Measurements (Veterinary Validated Bounds)
    heart_rate: Optional[int] = Field(
        None, 
        ge=30, le=250, 
        description="Maps to dwc:measurementType 'heart rate'. Bounds 30-250 BPM accommodate resting giant breeds to stressed/exercising puppies [16-19]."
    )
    heart_rate_unit: Literal["BPM"] = Field(
        "BPM", 
        description="Maps to dwc:measurementUnit [6, 20]."
    )
    body_temp: Optional[float] = Field(
        None, 
        ge=35.0, le=40.0, 
        description="Maps to dwc:measurementType 'body temperature'. Evaluates bounds ranging from neonatal hypothermia (35.0°C) to fever states (>39.4°C) [21, 22]."
    )
    temp_unit: Literal["°C"] = Field(
        "°C", 
        description="Maps to dwc:measurementUnit [6, 20]."
    )
    respiratory_rate: Optional[int] = Field(
        None, 
        ge=10, le=50, 
        description="Maps to dwc:measurementType 'respiratory rate'. Accommodates normal resting ranges (18-34 breaths/min) to highly elevated states indicating pain or stress [23, 24]."
    )
    respiratory_rate_unit: Literal["breaths/min"] = Field(
        "breaths/min", 
        description="Maps to dwc:measurementUnit. Unit of measurement for respiratory rate."
    )

    # 5. Methodological Classification (Darwin Core Mapped)
    observation_method: Literal["HumanObservation", "MachineObservation"] = Field(
        ..., 
        description="Maps to dwc:basisOfRecord. Distinguishes between visual ethogram coding and sensor-derived data [5-7, 25]."
    )
    
    # 6. Raw Data Traceability 
    narrative: str = Field(
        ..., 
        description="Unstructured narrative report from which structured data was deterministically parsed [26, 27]."
    )