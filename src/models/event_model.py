"""
Event model - Event and Event Interest database operations
"""

from database import get_db_connection, get_db_cursor


def create_event_in_db(name, description, date_obj, organisation_id=None):
    """Insert event into database and return the created event"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """INSERT INTO events (name, description, date, organisation_id, interested_count) 
               VALUES (%s, %s, %s, %s, 0) 
               RETURNING id, name, description, date, organisation_id, interested_count""",
            (name, description, date_obj, organisation_id),
        )
        result = cursor.fetchone()
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def check_event_exists_by_name(name):
    """Check if an event with the given name exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM events WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def check_event_exists_by_id(event_id):
    """Check if an event with the given ID exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM events WHERE id = %s", (event_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def delete_event_from_db(event_id):
    """Delete event from database, returns True if deleted"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count > 0
    finally:
        cursor.close()
        conn.close()


def get_event_by_id_from_db(event_id):
    """Get a specific event by ID"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT id, name, description, date, organisation_id, interested_count FROM events WHERE id = %s",
            (event_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_events_from_db(name_filter=None, date_obj=None):
    """Get all events with optional filters"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        query = "SELECT id, name, description, date, organisation_id, interested_count FROM events WHERE 1=1"
        params = []

        if name_filter:
            query += " AND LOWER(name) LIKE LOWER(%s)"
            params.append(f"%{name_filter}%")

        if date_obj:
            query += " AND date = %s"
            params.append(date_obj)

        query += " ORDER BY date ASC"

        cursor.execute(query, params)
        events = cursor.fetchall()
        return events
    finally:
        cursor.close()
        conn.close()


# ============= EVENT INTEREST OPERATIONS =============


def check_user_interest_exists(user_id, event_id):
    """Check if a user is already interested in an event"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT id FROM event_interest WHERE user_id = %s AND event_id = %s",
            (user_id, event_id),
        )
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def add_user_interest_in_event(user_id, event_id):
    """Add user interest in an event and increment interested_count"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        # Insert interest record
        cursor.execute(
            "INSERT INTO event_interest (user_id, event_id) VALUES (%s, %s)",
            (user_id, event_id),
        )

        # Update interested_count
        cursor.execute(
            "UPDATE events SET interested_count = interested_count + 1 WHERE id = %s",
            (event_id,),
        )

        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def remove_user_interest_in_event(user_id, event_id):
    """Remove user interest in an event and decrement interested_count"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        # Delete interest record
        cursor.execute(
            "DELETE FROM event_interest WHERE user_id = %s AND event_id = %s",
            (user_id, event_id),
        )
        deleted_count = cursor.rowcount

        if deleted_count > 0:
            # Update interested_count
            cursor.execute(
                "UPDATE events SET interested_count = interested_count - 1 WHERE id = %s",
                (event_id,),
            )

        conn.commit()
        return deleted_count > 0
    finally:
        cursor.close()
        conn.close()
