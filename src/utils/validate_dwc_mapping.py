import sys

from src.pipeline.models import MeasurementOrFact


def validate():
    # Verify MeasurementOrFact fields have correct DwC serialization_aliases
    expected_mappings = {
        "individual_id": "dwc:individualID",
        "event_date": "dwc:eventDate",
        "measurement_type": "dwc:measurementType",
        "measurement_value": "dwc:measurementValue",
        "basis_of_record": "dwc:basisOfRecord",
    }

    for field_name, expected_alias in expected_mappings.items():
        field_info = MeasurementOrFact.model_fields.get(field_name)
        if not field_info:
            print(
                f"Error: MeasurementOrFact is missing required field '{field_name}'",
                file=sys.stderr,
            )
            sys.exit(1)

        alias = field_info.serialization_alias
        if alias != expected_alias:
            print(
                f"Error: Field '{field_name}' in MeasurementOrFact must map to "
                f"DwC term '{expected_alias}' (got '{alias}')",
                file=sys.stderr,
            )
            sys.exit(1)

    print("DwC mapping validation passed successfully.")


if __name__ == "__main__":
    validate()
