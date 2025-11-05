"""
Organisation service - Business logic for organisations
"""

from models.organisation_model import (
    create_organisation_in_db,
    check_organisation_exists_by_name,
    get_organisations_from_db,
)
from models.user_model import check_user_exists
from models.location_model import check_municipality_exists, check_parish_exists


def validate_organisation_data(data):
    """Validate organisation creation data"""
    # Check required fields
    if not data.get("name") or not data.get("head_user_id"):
        return False, "Missing required fields: name, head_user_id"

    # Check that at least one location is specified
    allowed_municipality_ids = data.get("allowed_municipality_ids", [])
    allowed_parish_ids = data.get("allowed_parish_ids", [])

    if not allowed_municipality_ids and not allowed_parish_ids:
        return False, "At least one allowed municipality or parish must be specified"

    return True, None


def create_organisation(data):
    """
    Create a new organisation
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Validate organisation data
    is_valid, error = validate_organisation_data(data)
    if not is_valid:
        return False, error, 400

    # Check if organisation name already exists
    if check_organisation_exists_by_name(data["name"]):
        return False, "An organisation with this name already exists", 409

    # Verify head user exists
    if not check_user_exists(data["head_user_id"]):
        return False, "User in charge not found", 404

    # Get and verify municipalities
    allowed_municipality_ids = data.get("allowed_municipality_ids", [])
    for mun_id in allowed_municipality_ids:
        if not check_municipality_exists(mun_id):
            return False, f"Municipality with id {mun_id} not found", 404

    # Get and verify parishes
    allowed_parish_ids = data.get("allowed_parish_ids", [])
    for parish_id in allowed_parish_ids:
        if not check_parish_exists(parish_id):
            return False, f"Parish with id {parish_id} not found", 404

    # Create organisation
    organisation_data = create_organisation_in_db(
        data["name"],
        data.get("description"),
        data["head_user_id"],
        allowed_municipality_ids,
        allowed_parish_ids,
    )

    return (
        True,
        {
            "message": "Organisation created successfully",
            "organisation": organisation_data,
        },
        201,
    )


def get_organisations():
    """
    Get all organisations
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    organisations = get_organisations_from_db()
    return (
        True,
        {"organisations": [org for org in organisations], "count": len(organisations)},
        200,
    )
