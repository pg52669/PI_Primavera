"""
Transport service - Business logic for transport requests
"""

from models.transport_model import (
    create_transport_request,
    check_transport_request_exists,
    get_transport_requests_by_event,
    delete_transport_request,
)
from models.event_model import check_event_exists_by_id
from models.user_model import check_user_exists
from models.volunteer_model import check_association_exists


def create_transport_request_service(event_id, user_id, requested_by_volunteer_id=None):
    """
    Create a transport request for an event
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify event exists
    if not check_event_exists_by_id(event_id):
        return False, "Event not found", 404

    # Verify user exists
    if not check_user_exists(user_id):
        return False, "User not found", 404

    # If requested by volunteer, verify association exists
    if requested_by_volunteer_id:
        if not check_user_exists(requested_by_volunteer_id):
            return False, "Volunteer not found", 404

        if not check_association_exists(requested_by_volunteer_id, user_id):
            return (
                False,
                "User is not associated with this volunteer",
                403,
            )

    # Check if request already exists
    if check_transport_request_exists(event_id, user_id):
        return False, "Transport request already exists for this user and event", 409

    # Create transport request
    try:
        result = create_transport_request(event_id, user_id, requested_by_volunteer_id)
        return (
            True,
            {
                "message": "Transport request created successfully",
                "transport_request": result,
            },
            201,
        )
    except Exception as e:
        return False, f"Failed to create transport request: {str(e)}", 500


def create_transport_request_for_assisted(event_id, volunteer_id, assisted_id):
    """
    Create a transport request for an assisted user (by their volunteer)
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify volunteer exists
    if not check_user_exists(volunteer_id):
        return False, "Volunteer not found", 404

    # Verify assisted user exists
    if not check_user_exists(assisted_id):
        return False, "Assisted user not found", 404

    # Verify event exists
    if not check_event_exists_by_id(event_id):
        return False, "Event not found", 404

    # Verify association exists
    if not check_association_exists(volunteer_id, assisted_id):
        return False, "User is not associated with this volunteer", 403

    # Check if request already exists
    if check_transport_request_exists(event_id, assisted_id):
        return False, "Transport request already exists for this user and event", 409

    # Create transport request (for the assisted user, requested by volunteer)
    try:
        result = create_transport_request(event_id, assisted_id, volunteer_id)
        return (
            True,
            {
                "message": "Transport request created successfully for assisted user",
                "transport_request": result,
            },
            201,
        )
    except Exception as e:
        return False, f"Failed to create transport request: {str(e)}", 500


def get_transport_requests(event_id):
    """
    Get all transport requests for an event
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify event exists
    if not check_event_exists_by_id(event_id):
        return False, "Event not found", 404

    # Get transport requests
    requests = get_transport_requests_by_event(event_id)

    return (
        True,
        {
            "transport_requests": [req for req in requests],
            "count": len(requests),
        },
        200,
    )

