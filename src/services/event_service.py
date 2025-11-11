"""
Event service - Business logic for events
"""

from utils.validators import validate_required_fields, validate_date_format
from utils.formatters import format_event
from models.event_model import (
    create_event_in_db,
    check_event_exists_by_name,
    check_event_exists_by_id,
    delete_event_from_db,
    get_events_from_db,
    get_event_by_id_from_db,
    check_user_interest_exists,
    add_user_interest_in_event,
    remove_user_interest_in_event,
)
from models.organisation_model import check_organisation_exists_by_id
from models.user_model import check_user_exists
from models.volunteer_model import check_association_exists, get_assisted_users_by_volunteer


def validate_event_data(data):
    """Validate event creation data"""
    # Check required fields
    required = ["name", "description", "date"]
    is_valid, error = validate_required_fields(data, required)
    if not is_valid:
        return False, error

    # Validate date format
    is_valid, date_obj, error = validate_date_format(data["date"])
    if not is_valid:
        return False, error

    return True, None


def create_event(data):
    """
    Create a new event
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Validate event data
    is_valid, error = validate_event_data(data)
    if not is_valid:
        return False, error, 400

    # Check if event name already exists
    if check_event_exists_by_name(data["name"]):
        return False, "An event with this name already exists", 409

    # If organisation_id is provided, verify it exists
    organisation_id = data.get("organisation_id")
    if organisation_id and not check_organisation_exists_by_id(organisation_id):
        return False, "Organisation not found", 404

    # Parse date
    is_valid, date_obj, error = validate_date_format(data["date"])
    if not is_valid:
        return False, error, 400

    # Create event
    result = create_event_in_db(
        data["name"], data["description"], date_obj, organisation_id
    )

    if not result:
        return False, "Failed to create event", 500

    # Format and return event
    event = format_event(result)
    return True, {"message": "Event created successfully", "event": event}, 201


def delete_event(event_id):
    """
    Delete an event by ID
    Returns: (success: bool, message: str, status_code: int)
    """
    if not event_id:
        return False, "Missing required field: id", 400

    # Delete event
    deleted = delete_event_from_db(event_id)

    if not deleted:
        return False, "Event not found", 404

    return True, "Event deleted successfully", 200


def get_events(name_filter=None, date_filter=None):
    """
    Get all events with optional filters
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Parse date filter if provided
    date_obj = None
    if date_filter:
        is_valid, date_obj, error = validate_date_format(date_filter)
        if not is_valid:
            return False, error, 400

    # Get events
    events = get_events_from_db(name_filter, date_obj)

    # Format events
    formatted_events = [format_event(event) for event in events]

    return True, {"events": formatted_events, "count": len(formatted_events)}, 200


def mark_user_interest(event_id, user_id):
    """
    Mark a user as interested in an event
    Returns: (success: bool, message: str, status_code: int)
    """
    if not user_id:
        return False, "Missing required field: user_id", 400

    # Verify user exists
    if not check_user_exists(user_id):
        return False, "User not found", 404

    # Verify event exists
    if not check_event_exists_by_id(event_id):
        return False, "Event not found", 404

    # Check if already interested
    if check_user_interest_exists(user_id, event_id):
        return True, "User is already interested in this event", 200

    # Add interest
    add_user_interest_in_event(user_id, event_id)

    return True, "Interest registered successfully", 201


def remove_user_interest(event_id, user_id):
    """
    Remove a user's interest in an event
    Returns: (success: bool, message: str, status_code: int)
    """
    if not user_id:
        return False, "Missing required field: user_id", 400

    # Remove interest
    removed = remove_user_interest_in_event(user_id, event_id)

    if not removed:
        return False, "User was not interested in this event", 404

    return True, "Interest removed successfully", 200


def mark_interest_for_assisted(event_id, volunteer_id, assisted_id):
    """
    Mark an assisted user as interested in an event (by their volunteer)
    Returns: (success: bool, message: str, status_code: int)
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

    # Check if already interested
    if check_user_interest_exists(assisted_id, event_id):
        return True, "User is already interested in this event", 200

    # Add interest (for the assisted user)
    add_user_interest_in_event(assisted_id, event_id)

    return True, "Interest registered successfully for assisted user", 201


def get_event_by_id(event_id):
    """
    Get a specific event by ID
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Get event details
    event = get_event_by_id_from_db(event_id)

    if not event:
        return False, "Event not found", 404

    # Format event
    formatted_event = format_event(event)

    return True, {"event": formatted_event}, 200
