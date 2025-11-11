"""
Message service - Business logic for in-app messaging
"""

from models.message_model import create_message, get_messages_for_user
from models.user_model import check_user_exists
from models.volunteer_model import check_association_exists, check_user_is_assisted, get_volunteer_by_assisted


def send_message(sender_id, receiver_id, message_text):
    """
    Send a message between users
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Validate message
    if not message_text or not message_text.strip():
        return False, "Message cannot be empty", 400

    # Verify users exist
    if not check_user_exists(sender_id):
        return False, "Sender not found", 404

    if not check_user_exists(receiver_id):
        return False, "Receiver not found", 404

    # Check if users can communicate
    # Volunteers can message their assisted users
    # Assisted users can message their volunteer
    can_communicate = False

    # Check if sender is volunteer and receiver is assisted
    if check_association_exists(sender_id, receiver_id):
        can_communicate = True

    # Check if sender is assisted and receiver is volunteer
    volunteer = get_volunteer_by_assisted(sender_id)
    if volunteer and volunteer["id"] == receiver_id:
        can_communicate = True

    if not can_communicate:
        return (
            False,
            "Users can only communicate if they have a volunteer-assisted relationship",
            403,
        )

    # Create message
    try:
        result = create_message(sender_id, receiver_id, message_text.strip())
        return (
            True,
            {
                "message": "Message sent successfully",
                "message_data": result,
            },
            201,
        )
    except Exception as e:
        return False, f"Failed to send message: {str(e)}", 500


def get_user_messages(user_id):
    """
    Get all messages for a user
    Returns: (success: bool, result: dict/str, status_code: int)
    """
    # Verify user exists
    if not check_user_exists(user_id):
        return False, "User not found", 404

    # Get messages
    messages = get_messages_for_user(user_id)

    return (
        True,
        {
            "messages": [msg for msg in messages],
            "count": len(messages),
        },
        200,
    )

