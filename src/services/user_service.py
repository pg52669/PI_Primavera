"""
User service - Business logic for users
"""

from utils.validators import validate_required_fields, validate_gender
from models.user_model import (
    check_user_exists,
    create_user_in_db,
    get_users_from_db,
    delete_user_from_db,
)
from models.organisation_model import check_organisation_exists_by_id


def validate_user_data(data):
    """Validate user creation data"""
    # Check required fields
    required = [
        "name",
        "age",
        "gender",
        "street",
        "street_number",
        "postal_code",
        "city",
    ]
    is_valid, error = validate_required_fields(data, required)
    if not is_valid:
        return False, error

    # Validate gender
    is_valid, error = validate_gender(data["gender"])
    if not is_valid:
        return False, error

    return True, None


def create_user(data):
    """
    Create a new user
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Validate user data
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return False, error, 400

    # If organisation_id is provided, verify it exists
    organisation_id = data.get("organisation_id")
    if organisation_id and not check_organisation_exists_by_id(organisation_id):
        return False, "Organisation not found", 404

    # Create user
    result = create_user_in_db(data)

    if not result:
        return False, "Failed to create user", 500

    return True, {"message": "User created successfully", "user": result}, 201


def get_users():
    """
    Get all users
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    users = get_users_from_db()
    return True, {"users": [user for user in users], "count": len(users)}, 200


def delete_user(user_id):
    """
    Delete a user by ID
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Check if user exists first
    if not check_user_exists(user_id):
        return False, "User not found", 404

    # Delete the user
    success = delete_user_from_db(user_id)

    if not success:
        return False, "Failed to delete user", 500

    return True, {"message": f"User with ID {user_id} deleted successfully"}, 200
