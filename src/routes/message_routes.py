"""
Message routes - HTTP endpoints for in-app messaging
"""

from flask import Blueprint, request, jsonify
from utils.validators import extract_request_data
from services.message_service import send_message, get_user_messages

message_api = Blueprint("messages", __name__)


@message_api.route("/messages", methods=["POST"])
def send_message_route():
    """Send a message"""
    try:
        data = extract_request_data(request)
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        message = data.get("message")

        if not sender_id or not receiver_id or not message:
            return (
                jsonify(
                    {"error": "Missing required fields: sender_id, receiver_id, message"}
                ),
                400,
            )

        success, result, status_code = send_message(sender_id, receiver_id, message)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@message_api.route("/messages", methods=["GET"])
def get_messages_route():
    """Get all messages for a user"""
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "Missing required parameter: user_id"}), 400

        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user_id format"}), 400

        success, result, status_code = get_user_messages(user_id)

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

