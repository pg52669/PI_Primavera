"""
Transport model - Transport request operations
"""

from database import get_db_connection, get_db_cursor


def create_transport_request(event_id, user_id, requested_by_volunteer_id=None):
    """Create a transport request for an event"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """INSERT INTO event_transport_requests (event_id, user_id, requested_by_volunteer_id)
               VALUES (%s, %s, %s)
               RETURNING id, event_id, user_id, requested_by_volunteer_id, created_at""",
            (event_id, user_id, requested_by_volunteer_id),
        )
        result = cursor.fetchone()
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def check_transport_request_exists(event_id, user_id):
    """Check if transport request already exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT id FROM event_transport_requests WHERE event_id = %s AND user_id = %s",
            (event_id, user_id),
        )
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_transport_requests_by_event(event_id):
    """Get all transport requests for an event"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """SELECT etr.id, etr.user_id, etr.requested_by_volunteer_id, etr.created_at,
                      u.name as user_name, u.age as user_age, u.city as user_city,
                      v.name as volunteer_name
               FROM event_transport_requests etr
               JOIN users u ON etr.user_id = u.id
               LEFT JOIN users v ON etr.requested_by_volunteer_id = v.id
               WHERE etr.event_id = %s
               ORDER BY etr.created_at DESC""",
            (event_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def delete_transport_request(event_id, user_id):
    """Delete a transport request"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        cursor.execute(
            "DELETE FROM event_transport_requests WHERE event_id = %s AND user_id = %s",
            (event_id, user_id),
        )
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count > 0
    finally:
        cursor.close()
        conn.close()

