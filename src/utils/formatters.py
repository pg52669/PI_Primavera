"""
Data formatting utilities
"""


def format_date(date_obj):
    """Format a date object to dd-MM-yyyy string"""
    if date_obj is None:
        return None
    return date_obj.strftime("%d-%m-%Y")


def format_event(event):
    """Format an event record for API response"""
    return {
        "id": event["id"],
        "name": event["name"],
        "description": event["description"],
        "date": format_date(event["date"]),
        "organisation_id": event["organisation_id"],
        "interested_count": event["interested_count"],
    }
