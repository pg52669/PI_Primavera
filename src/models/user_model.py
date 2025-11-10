"""
User model - User database operations
"""

from database import get_db_connection, get_db_cursor


def create_user_in_db(data):
    """Insert user into database and return the created user"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """INSERT INTO users (name, age, gender, street, street_number, apartment, postal_code, city, 
               is_volunteer, is_assisted, has_organisation, organisation_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
               RETURNING id, name, age, gender, street, street_number, apartment, postal_code, city, 
               is_volunteer, is_assisted, has_organisation, organisation_id""",
            (
                data["name"],
                data["age"],
                data["gender"],
                data["street"],
                data["street_number"],
                data.get("apartment"),
                data["postal_code"],
                data["city"],
                data.get("is_volunteer", False),
                data.get("is_assisted", False),
                data.get("has_organisation", False),
                data.get("organisation_id"),
            ),
        )
        result = cursor.fetchone()
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def check_user_exists(user_id):
    """Check if a user exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_users_from_db():
    """Get all users"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT * FROM users ORDER BY id ASC")
        users = cursor.fetchall()
        return users
    finally:
        cursor.close()
        conn.close()


def delete_user_from_db(user_id):
    """Delete a user from database"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        deleted_rows = cursor.rowcount
        conn.commit()
        return deleted_rows > 0
    finally:
        cursor.close()
        conn.close()
