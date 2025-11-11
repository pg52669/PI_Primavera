"""
Message model - In-app messaging operations
"""

from database import get_db_connection, get_db_cursor


def create_message(sender_id, receiver_id, message):
    """Create a new message"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """INSERT INTO messages (sender_id, receiver_id, message)
               VALUES (%s, %s, %s)
               RETURNING id, sender_id, receiver_id, message, is_read, created_at""",
            (sender_id, receiver_id, message),
        )
        result = cursor.fetchone()
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def get_messages_for_user(user_id):
    """Get all messages received by a user, grouped by sender"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """SELECT m.id, m.sender_id, m.receiver_id, m.message, m.is_read, m.created_at,
                      u.name as sender_name, u.city as sender_city
               FROM messages m
               JOIN users u ON m.sender_id = u.id
               WHERE m.receiver_id = %s
               ORDER BY m.created_at DESC""",
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def mark_message_as_read(message_id, user_id):
    """Mark a message as read"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        cursor.execute(
            "UPDATE messages SET is_read = TRUE WHERE id = %s AND receiver_id = %s",
            (message_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

