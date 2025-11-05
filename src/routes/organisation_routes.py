"""
Organisation routes - HTTP endpoints for organisations
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.organisation_service import (
    create_organisation as create_organisation_service,
    get_organisations as get_organisations_service,
)

organisations_api = Blueprint("organisations", __name__)


@organisations_api.route("/organisation", methods=["POST"])
def create_organisation():
    """Create a new organisation"""
    try:
        data = extract_request_data(request)
        success, result, status_code = create_organisation_service(data)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@organisations_api.route("/organisations", methods=["GET"])
def get_organisations():
    """Get all organisations with their allowed locations"""
    try:
        success, result, status_code = get_organisations_service()

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
