"""
Volunteer service - Business logic for volunteer-assisted relationships
"""

from models.volunteer_model import (
    get_or_create_user_code,
    get_user_code,
    get_user_by_code,
    associate_volunteer_assisted,
    disassociate_volunteer_assisted,
    get_assisted_users_by_volunteer,
    get_volunteer_by_assisted,
    check_user_is_assisted,
    check_association_exists,
)
from models.user_model import check_user_exists


def get_user_qr_code(user_id):
    """
    Get or generate QR code for a user
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify user exists
    if not check_user_exists(user_id):
        return False, "User not found", 404

    # Check if user is already assisted (can't have active QR code)
    volunteer_id = check_user_is_assisted(user_id)
    if volunteer_id:
        return False, "Assisted users cannot have active QR codes", 403

    # Get or create code
    code = get_or_create_user_code(user_id)

    return True, {"user_id": user_id, "code": code}, 200


def associate_by_code(volunteer_id, code):
    """
    Associate a volunteer with an assisted user using QR code
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify volunteer exists
    if not check_user_exists(volunteer_id):
        return False, "Volunteer not found", 404

    # Check if volunteer is already assisted (can't read codes)
    if check_user_is_assisted(volunteer_id):
        return False, "Assisted users cannot read QR codes", 403

    # Get user by code
    assisted_id = get_user_by_code(code)
    if not assisted_id:
        return False, "Invalid QR code", 404

    # Verify assisted user exists
    if not check_user_exists(assisted_id):
        return False, "User associated with code not found", 404

    # Check if user is already assisted
    if check_user_is_assisted(assisted_id):
        return False, "This user is already associated with a volunteer", 409

    # Check if trying to associate with self
    if volunteer_id == assisted_id:
        return False, "Cannot associate user with themselves", 400

    # Create association
    try:
        associate_volunteer_assisted(volunteer_id, assisted_id)
        return (
            True,
            {
                "message": "Successfully associated volunteer with assisted user",
                "volunteer_id": volunteer_id,
                "assisted_id": assisted_id,
            },
            201,
        )
    except Exception as e:
        return False, f"Failed to create association: {str(e)}", 500


def disassociate(volunteer_id, assisted_id, confirmation):
    """
    Disassociate a volunteer from an assisted user
    Returns: (success: bool, message: str, status_code: int)
    """
    # Verify confirmation
    if confirmation.upper() != "CONFIRMAR":
        return False, "Invalid confirmation. Please type 'CONFIRMAR' to confirm", 400

    # Verify users exist
    if not check_user_exists(volunteer_id):
        return False, "Volunteer not found", 404

    if not check_user_exists(assisted_id):
        return False, "Assisted user not found", 404

    # Check if association exists
    if not check_association_exists(volunteer_id, assisted_id):
        return False, "Association not found", 404

    # Disassociate
    try:
        disassociate_volunteer_assisted(volunteer_id, assisted_id)
        return True, "Successfully disassociated volunteer from assisted user", 200
    except Exception as e:
        return False, f"Failed to disassociate: {str(e)}", 500


def get_assisted_users(volunteer_id):
    """
    Get all assisted users for a volunteer
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify volunteer exists
    if not check_user_exists(volunteer_id):
        return False, "Volunteer not found", 404

    # Get assisted users
    assisted_users = get_assisted_users_by_volunteer(volunteer_id)

    return (
        True,
        {
            "assisted_users": [user for user in assisted_users],
            "count": len(assisted_users),
        },
        200,
    )


def get_volunteer_for_assisted(assisted_id):
    """
    Get volunteer for an assisted user
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify assisted user exists
    if not check_user_exists(assisted_id):
        return False, "Assisted user not found", 404

    # Get volunteer
    volunteer = get_volunteer_by_assisted(assisted_id)

    if not volunteer:
        return False, "No volunteer associated with this user", 404

    return True, {"volunteer": volunteer}, 200

