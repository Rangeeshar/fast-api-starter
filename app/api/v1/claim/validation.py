"""
Validation for fields for a request
"""
from app.common.api_exceptions import RequestError


def validate_fields(field_data_list):
    # Validate each field with flexible logic
    for field in field_data_list:
        if field.get("name") == "submitted_procedure":
            if not field.get("value").startswith("D"):
                raise RequestError(
                    status_code=400,
                    error_code="FV-01",
                    error_msg="submitted_procedure should start with D",
                )
        if field.get("name") == "provider_npi":
            if not len(str(field.get("value", ""))) != 10:
                raise RequestError(
                    status_code=400,
                    error_code="FV-01",
                    error_msg="provider_npi should have exactly 10 digits",
                )
