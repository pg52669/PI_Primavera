"""
Database models package - all SQL operations
"""

from .event_model import (
    create_event_in_db,
    check_event_exists_by_name,
    check_event_exists_by_id,
    delete_event_from_db,
    get_events_from_db,
    check_user_interest_exists,
    add_user_interest_in_event,
    remove_user_interest_in_event,
)
from .user_model import (
    create_user_in_db,
    check_user_exists,
    get_users_from_db,
)
from .organisation_model import (
    create_organisation_in_db,
    check_organisation_exists_by_name,
    check_organisation_exists_by_id,
    get_organisations_from_db,
)
from .location_model import (
    check_municipality_exists,
    check_parish_exists,
    get_districts_from_db,
    get_municipalities_from_db,
    get_parishes_from_db,
)

__all__ = [
    # Event operations
    "create_event_in_db",
    "check_event_exists_by_name",
    "check_event_exists_by_id",
    "delete_event_from_db",
    "get_events_from_db",
    "check_user_interest_exists",
    "add_user_interest_in_event",
    "remove_user_interest_in_event",
    # User operations
    "create_user_in_db",
    "check_user_exists",
    "get_users_from_db",
    # Organisation operations
    "create_organisation_in_db",
    "check_organisation_exists_by_name",
    "check_organisation_exists_by_id",
    "get_organisations_from_db",
    # Location operations
    "check_municipality_exists",
    "check_parish_exists",
    "get_districts_from_db",
    "get_municipalities_from_db",
    "get_parishes_from_db",
]
