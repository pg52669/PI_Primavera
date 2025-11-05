"""
Location model - District, Municipality, and Parish database operations
"""

from database import get_db_connection, get_db_cursor


def check_municipality_exists(municipality_id):
    """Check if a municipality exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            "SELECT id FROM municipalities WHERE id = %s", (municipality_id,)
        )
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def check_parish_exists(parish_id):
    """Check if a parish exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM parishes WHERE id = %s", (parish_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_districts_from_db():
    """Get all districts"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT * FROM districts ORDER BY name ASC")
        districts = cursor.fetchall()
        return districts
    finally:
        cursor.close()
        conn.close()


def get_municipalities_from_db(district_id=None):
    """Get all municipalities, optionally filtered by district"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        if district_id:
            cursor.execute(
                """SELECT m.*, d.name as district_name 
                   FROM municipalities m
                   JOIN districts d ON m.district_id = d.id
                   WHERE m.district_id = %s 
                   ORDER BY m.name ASC""",
                (district_id,),
            )
        else:
            cursor.execute(
                """SELECT m.*, d.name as district_name 
                   FROM municipalities m
                   JOIN districts d ON m.district_id = d.id
                   ORDER BY m.name ASC"""
            )
        municipalities = cursor.fetchall()
        return municipalities
    finally:
        cursor.close()
        conn.close()


def get_parishes_from_db(municipality_id=None):
    """Get all parishes, optionally filtered by municipality"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        if municipality_id:
            cursor.execute(
                """SELECT p.*, m.name as municipality_name, d.name as district_name
                   FROM parishes p
                   JOIN municipalities m ON p.municipality_id = m.id
                   JOIN districts d ON m.district_id = d.id
                   WHERE p.municipality_id = %s 
                   ORDER BY p.name ASC""",
                (municipality_id,),
            )
        else:
            cursor.execute(
                """SELECT p.*, m.name as municipality_name, d.name as district_name
                   FROM parishes p
                   JOIN municipalities m ON p.municipality_id = m.id
                   JOIN districts d ON m.district_id = d.id
                   ORDER BY p.name ASC"""
            )
        parishes = cursor.fetchall()
        return parishes
    finally:
        cursor.close()
        conn.close()
