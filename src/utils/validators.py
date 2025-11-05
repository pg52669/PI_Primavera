"""
Input validation utilities
"""

from datetime import datetime


def validate_required_fields(data, required_fields):
    """Validate that all required fields are present and non-empty"""
    for field in required_fields:
        if not data.get(field):
            return False, f"Missing required field: {field}"
    return True, None


def validate_date_format(date_str):
    """Validate and parse date in dd-MM-yyyy format"""
    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        return True, date_obj, None
    except ValueError:
        return False, None, "Invalid date format. Use dd-MM-yyyy"


def validate_gender(gender):
    """Validate gender field"""
    valid_genders = ["male", "female", "other"]
    if gender not in valid_genders:
        return False, f"Gender must be one of: {', '.join(valid_genders)}"
    return True, None


def extract_request_data(request):
    """Extract data from request (JSON or form)"""
    if request.is_json:
        return request.get_json()
    else:
        return request.form.to_dict()
