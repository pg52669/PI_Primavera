"""
Event routes - HTTP endpoints for events
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.event_service import (
    create_event as create_event_service,
    delete_event as delete_event_service,
    get_events as get_events_service,
    mark_user_interest,
    remove_user_interest,
)

events_api = Blueprint("events", __name__)


@events_api.route("/event", methods=["POST"])
def create_event():
    """Create a new event"""
    try:
        data = extract_request_data(request)
        success, result, status_code = create_event_service(data)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_api.route("/event", methods=["DELETE"])
def delete_event():
    """Delete an event by id"""
    try:
        event_id = request.form.get("id") or (request.get_json() or {}).get("id")
        success, message, status_code = delete_event_service(event_id)

        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_api.route("/events", methods=["GET"])
def get_events():
    """Get all events with optional filters"""
    try:
        name_filter = request.form.get("name") or request.args.get("name")
        date_filter = request.form.get("date") or request.args.get("date")

        success, result, status_code = get_events_service(name_filter, date_filter)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_api.route("/event/<int:event_id>/interest", methods=["POST"])
def mark_interest(event_id):
    """Mark a user as interested in an event"""
    try:
        data = extract_request_data(request)
        user_id = data.get("user_id")

        success, message, status_code = mark_user_interest(event_id, user_id)

        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_api.route("/event/<int:event_id>/interest", methods=["DELETE"])
def remove_interest(event_id):
    """Remove a user's interest in an event"""
    try:
        data = extract_request_data(request)
        user_id = data.get("user_id")

        success, message, status_code = remove_user_interest(event_id, user_id)

        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Events API is running"}), 200
