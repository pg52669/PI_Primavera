"""
User routes - HTTP endpoints for users
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.user_service import (
    create_user as create_user_service,
    get_users as get_users_service,
)

users_api = Blueprint("users", __name__)


@users_api.route("/user", methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        data = extract_request_data(request)
        success, result, status_code = create_user_service(data)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_api.route("/users", methods=["GET"])
def get_users():
    """Get all users"""
    try:
        success, result, status_code = get_users_service()

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
