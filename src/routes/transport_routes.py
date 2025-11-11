"""
Transport routes - HTTP endpoints for transport requests
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.transport_service import (
    create_transport_request_service,
    create_transport_request_for_assisted,
    get_transport_requests,
)

transport_api = Blueprint("transport", __name__)


@transport_api.route("/event/<int:event_id>/transport-request", methods=["POST"])
def create_transport_request_route(event_id):
    """Create a transport request for an event"""
    try:
        data = extract_request_data(request)
        user_id = data.get("user_id")
        requested_by_volunteer_id = data.get("requested_by_volunteer_id")

        if not user_id:
            return jsonify({"error": "Missing required field: user_id"}), 400

        success, result, status_code = create_transport_request_service(
            event_id, user_id, requested_by_volunteer_id
        )

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@transport_api.route("/event/<int:event_id>/transport-request/assisted", methods=["POST"])
def create_transport_request_assisted_route(event_id):
    """Create a transport request for an assisted user (by their volunteer)"""
    try:
        data = extract_request_data(request)
        volunteer_id = data.get("volunteer_id")
        assisted_id = data.get("assisted_id")

        if not volunteer_id or not assisted_id:
            return (
                jsonify({"error": "Missing required fields: volunteer_id, assisted_id"}),
                400,
            )

        success, result, status_code = create_transport_request_for_assisted(
            event_id, volunteer_id, assisted_id
        )

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@transport_api.route("/event/<int:event_id>/transport-requests", methods=["GET"])
def get_transport_requests_route(event_id):
    """Get all transport requests for an event"""
    try:
        success, result, status_code = get_transport_requests(event_id)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

