from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Literal, Optional, Union
from datetime import datetime

BEHAVIOR_ONTOLOGY_MAPPING = {
    "barks": "http://purl.obolibrary.org/obo/GO_0071625",
    "lunges": "http://purl.obolibrary.org/obo/GO_0002118",
    "cowers": "http://purl.obolibrary.org/obo/NBO_0000244",
    "stress_markers": "http://purl.obolibrary.org/obo/NBO_0000000",
    "neutral": "http://purl.obolibrary.org/obo/NBO_0000311",
    "play_bow": "http://purl.obolibrary.org/obo/NBO_0000109",
    "licking_of_lips": "http://purl.obolibrary.org/obo/NBO_0000038",
    "looking_away": "http://purl.obolibrary.org/obo/NBO_0000039",
    "no_aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "moderate_aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "serious_aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "stranger_directed_aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "owner_directed_aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "dog_directed_aggression_fear": "http://purl.obolibrary.org/obo/GO_0002118",
    "trainability": "http://purl.obolibrary.org/obo/NBO_0000287",
    "separation_related_behavior": "http://purl.obolibrary.org/obo/NBO_0000535",
    "growling": "http://purl.obolibrary.org/obo/GO_0071625",
    "whining": "http://purl.obolibrary.org/obo/GO_0071625",
    "panting": "http://purl.obolibrary.org/obo/SYMP_0000345",
    "yawning": "http://purl.obolibrary.org/obo/NBO_0000074",
    "avoidance": "http://purl.obolibrary.org/obo/NBO_0000635",
    
    # Title Case Mappings for robust lookup support
    "No Aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "Moderate Aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "Serious Aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "Play Bow": "http://purl.obolibrary.org/obo/NBO_0000109",
    "Licking of Lips": "http://purl.obolibrary.org/obo/NBO_0000038",
    "Looking Away": "http://purl.obolibrary.org/obo/NBO_0000039",
    "Stranger-Directed Aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "Owner-Directed Aggression": "http://purl.obolibrary.org/obo/GO_0002118",
    "Dog-Directed Aggression/Fear": "http://purl.obolibrary.org/obo/GO_0002118",
    "Trainability": "http://purl.obolibrary.org/obo/NBO_0000287",
    "Separation-Related Behavior": "http://purl.obolibrary.org/obo/NBO_0000535",
    "Growling": "http://purl.obolibrary.org/obo/GO_0071625",
    "Whining": "http://purl.obolibrary.org/obo/GO_0071625",
    "Panting": "http://purl.obolibrary.org/obo/SYMP_0000345",
    "Yawning": "http://purl.obolibrary.org/obo/NBO_0000074",
    "Avoidance": "http://purl.obolibrary.org/obo/NBO_0000635"
}

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
    dog_size_category: Optional[Literal["Toy", "Small", "Medium", "Large", "Giant", "Puppy"]] = Field(
        None,
        description="Dog size category used for size-adjusted physiological validation bounds [5-6]."
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
        "barks", "lunges", "cowers", "stress_markers", "neutral", "play_bow", "licking_of_lips", "looking_away",
        "No Aggression", "no_aggression",
        "Moderate Aggression", "moderate_aggression",
        "Serious Aggression", "serious_aggression",
        "Play Bow",
        "Licking of Lips",
        "Looking Away",
        "Stranger-Directed Aggression", "stranger_directed_aggression",
        "Owner-Directed Aggression", "owner_directed_aggression",
        "Dog-Directed Aggression/Fear", "dog_directed_aggression_fear",
        "Trainability", "trainability",
        "Separation-Related Behavior", "separation_related_behavior",
        "growling", "Growling",
        "whining", "Whining",
        "panting", "Panting",
        "yawning", "Yawning",
        "avoidance", "Avoidance"
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
    behavior_type_id: Optional[str] = Field(
        None,
        description="Maps to dwc:measurementTypeID. Standardized ontology URI for the behavioral category."
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
    cortisol_level: Optional[float] = Field(
        None,
        ge=0.0,
        description="Maps to dwc:measurementType 'cortisol'. Salivary, hair, fecal, or blood cortisol concentration [9]."
    )
    cortisol_unit: Literal["ng/mL"] = Field(
        "ng/mL",
        description="Maps to dwc:measurementUnit for cortisol levels."
    )
    cortisol_matrix: Optional[Literal["blood", "serum", "plasma", "saliva", "urine", "hair", "feces", "claws"]] = Field(
        None,
        description="Biological matrix used for the cortisol assay to enable standardized cross-study comparisons [9]."
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

    @model_validator(mode="after")
    def validate_size_dependent_heart_rate(self) -> "EthologicalObservation":
        if self.heart_rate is None or self.dog_size_category is None:
            return self

        size = self.dog_size_category
        hr = self.heart_rate

        limits = {
            "Toy": (80, 200),
            "Small": (70, 180),
            "Medium": (50, 140),
            "Large": (45, 120),
            "Giant": (40, 110),
            "Puppy": (100, 220),
        }

        min_val, max_val = limits[size]
        if not (min_val <= hr <= max_val):
            raise ValueError(
                f"Heart rate {hr} BPM is out of veterinary bounds for a {size} dog ({min_val}-{max_val} BPM)."
            )

        return self

    @model_validator(mode="after")
    def resolve_behavior_type_id(self) -> "EthologicalObservation":
        if (self.behavior_type_id is None or self.behavior_type_id == "") and self.behavior_type is not None:
            self.behavior_type_id = BEHAVIOR_ONTOLOGY_MAPPING.get(self.behavior_type)
        return self

