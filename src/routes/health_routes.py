"""
Health check routes - System health monitoring endpoints
"""

from flask import Blueprint, jsonify

health_api = Blueprint("health", __name__)


@health_api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for the API"""
    return jsonify({"status": "ok", "message": "Events API is running"}), 200
