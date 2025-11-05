"""
Location routes - HTTP endpoints for districts, municipalities, and parishes
"""

from flask import Blueprint, request, jsonify
from models.location_model import (
    get_districts_from_db,
    get_municipalities_from_db,
    get_parishes_from_db,
)

locations_api = Blueprint("locations", __name__)


@locations_api.route("/districts", methods=["GET"])
def get_districts():
    """Get all districts"""
    try:
        districts = get_districts_from_db()
        return jsonify(
            {"districts": [district for district in districts], "count": len(districts)}
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@locations_api.route("/municipalities", methods=["GET"])
def get_municipalities():
    """Get all municipalities, optionally filtered by district"""
    try:
        district_id = request.args.get("district_id")
        municipalities = get_municipalities_from_db(district_id)
        return jsonify(
            {
                "municipalities": [mun for mun in municipalities],
                "count": len(municipalities),
            }
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@locations_api.route("/parishes", methods=["GET"])
def get_parishes():
    """Get all parishes, optionally filtered by municipality"""
    try:
        municipality_id = request.args.get("municipality_id")
        parishes = get_parishes_from_db(municipality_id)
        return jsonify(
            {"parishes": [parish for parish in parishes], "count": len(parishes)}
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
