"""
Volunteer model - Volunteer-Assisted relationships and QR codes
"""

import secrets
import string
from database import get_db_connection, get_db_cursor


def generate_unique_code(length=8):
    """Generate a unique alphanumeric code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def get_or_create_user_code(user_id):
    """Get existing code for user or create a new one"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        # Check if user already has a code
        cursor.execute(
            "SELECT code FROM user_codes WHERE user_id = %s AND is_active = TRUE",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            return result["code"]

        # Generate new unique code
        max_attempts = 10
        for _ in range(max_attempts):
            code = generate_unique_code()
            try:
                cursor.execute(
                    "INSERT INTO user_codes (user_id, code) VALUES (%s, %s)",
                    (user_id, code)
                )
                conn.commit()
                return code
            except Exception:
                conn.rollback()
                continue

        raise Exception("Failed to generate unique code")
    finally:
        cursor.close()
        conn.close()


def get_user_code(user_id):
    """Get the QR code for a user"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT code FROM user_codes WHERE user_id = %s AND is_active = TRUE",
            (user_id,)
        )
        result = cursor.fetchone()
        return result["code"] if result else None
    finally:
        cursor.close()
        conn.close()


def get_user_by_code(code):
    """Get user ID by QR code"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT user_id FROM user_codes WHERE code = %s AND is_active = TRUE",
            (code,)
        )
        result = cursor.fetchone()
        return result["user_id"] if result else None
    finally:
        cursor.close()
        conn.close()


def deactivate_user_code(user_id):
    """Deactivate QR code for a user (when they become a volunteer)"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "UPDATE user_codes SET is_active = FALSE WHERE user_id = %s",
            (user_id,)
        )
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def check_user_is_volunteer(user_id):
    """Check if user is a volunteer (has assisted users)"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT COUNT(*) as count FROM volunteer_assisted WHERE volunteer_id = %s",
            (user_id,)
        )
        result = cursor.fetchone()
        return result["count"] > 0 if result else False
    finally:
        cursor.close()
        conn.close()


def check_user_is_assisted(user_id):
    """Check if user is assisted (has a volunteer)"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT volunteer_id FROM volunteer_assisted WHERE assisted_id = %s",
            (user_id,)
        )
        result = cursor.fetchone()
        return result["volunteer_id"] if result else None
    finally:
        cursor.close()
        conn.close()


def associate_volunteer_assisted(volunteer_id, assisted_id):
    """Associate a volunteer with an assisted user"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        # Create association
        cursor.execute(
            "INSERT INTO volunteer_assisted (volunteer_id, assisted_id) VALUES (%s, %s)",
            (volunteer_id, assisted_id)
        )

        # Update volunteer flag
        cursor.execute(
            "UPDATE users SET is_volunteer = TRUE WHERE id = %s",
            (volunteer_id,)
        )

        # Update assisted flag
        cursor.execute(
            "UPDATE users SET is_assisted = TRUE WHERE id = %s",
            (assisted_id,)
        )

        # Deactivate assisted user's QR code
        deactivate_user_code(assisted_id)

        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def disassociate_volunteer_assisted(volunteer_id, assisted_id):
    """Disassociate a volunteer from an assisted user"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn, dict_cursor=False)

    try:
        # Delete association
        cursor.execute(
            "DELETE FROM volunteer_assisted WHERE volunteer_id = %s AND assisted_id = %s",
            (volunteer_id, assisted_id)
        )
        deleted_count = cursor.rowcount

        if deleted_count > 0:
            # Update assisted flag
            cursor.execute(
                "UPDATE users SET is_assisted = FALSE WHERE id = %s",
                (assisted_id,)
            )

            # Check if volunteer has other assisted users
            cursor.execute(
                "SELECT COUNT(*) FROM volunteer_assisted WHERE volunteer_id = %s",
                (volunteer_id,)
            )
            remaining_count = cursor.fetchone()[0]

            # Update volunteer flag if no more assisted users
            if remaining_count == 0:
                cursor.execute(
                    "UPDATE users SET is_volunteer = FALSE WHERE id = %s",
                    (volunteer_id,)
                )

        conn.commit()
        return deleted_count > 0
    finally:
        cursor.close()
        conn.close()


def get_assisted_users_by_volunteer(volunteer_id):
    """Get all assisted users for a volunteer"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """SELECT u.id, u.name, u.age, u.gender, u.city, va.created_at
               FROM users u
               JOIN volunteer_assisted va ON u.id = va.assisted_id
               WHERE va.volunteer_id = %s
               ORDER BY va.created_at DESC""",
            (volunteer_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_volunteer_by_assisted(assisted_id):
    """Get volunteer for an assisted user"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """SELECT u.id, u.name, u.age, u.gender, u.city, va.created_at
               FROM users u
               JOIN volunteer_assisted va ON u.id = va.volunteer_id
               WHERE va.assisted_id = %s""",
            (assisted_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def check_association_exists(volunteer_id, assisted_id):
    """Check if association exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT id FROM volunteer_assisted WHERE volunteer_id = %s AND assisted_id = %s",
            (volunteer_id, assisted_id)
        )
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()

