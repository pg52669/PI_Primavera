"""
Volunteer routes - HTTP endpoints for volunteer-assisted relationships
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.volunteer_service import (
    get_user_qr_code,
    associate_by_code,
    disassociate,
    get_assisted_users,
    get_volunteer_for_assisted,
)

volunteer_api = Blueprint("volunteer", __name__)


@volunteer_api.route("/user/<int:user_id>/code", methods=["GET"])
def get_code(user_id):
    """Get or generate QR code for a user"""
    try:
        success, result, status_code = get_user_qr_code(user_id)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@volunteer_api.route("/volunteer/associate", methods=["POST"])
def associate():
    """Associate a volunteer with an assisted user using QR code"""
    try:
        data = extract_request_data(request)
        volunteer_id = data.get("volunteer_id")
        code = data.get("code")

        if not volunteer_id or not code:
            return jsonify({"error": "Missing required fields: volunteer_id, code"}), 400

        success, result, status_code = associate_by_code(volunteer_id, code)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@volunteer_api.route("/volunteer/disassociate", methods=["POST"])
def disassociate_route():
    """Disassociate a volunteer from an assisted user"""
    try:
        data = extract_request_data(request)
        volunteer_id = data.get("volunteer_id")
        assisted_id = data.get("assisted_id")
        confirmation = data.get("confirmation")

        if not volunteer_id or not assisted_id or not confirmation:
            return (
                jsonify(
                    {
                        "error": "Missing required fields: volunteer_id, assisted_id, confirmation"
                    }
                ),
                400,
            )

        success, message, status_code = disassociate(volunteer_id, assisted_id, confirmation)

        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@volunteer_api.route("/volunteer/<int:volunteer_id>/assisted-users", methods=["GET"])
def get_assisted_users_route(volunteer_id):
    """Get all assisted users for a volunteer"""
    try:
        success, result, status_code = get_assisted_users(volunteer_id)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@volunteer_api.route("/assisted/<int:assisted_id>/volunteer", methods=["GET"])
def get_volunteer_route(assisted_id):
    """Get volunteer for an assisted user"""
    try:
        success, result, status_code = get_volunteer_for_assisted(assisted_id)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

