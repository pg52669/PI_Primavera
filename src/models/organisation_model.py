"""
Organisation model - Organisation database operations
"""

from database import get_db_connection, get_db_cursor


def create_organisation_in_db(
    name, description, head_user_id, allowed_municipality_ids, allowed_parish_ids
):
    """Insert organisation into database and return the created organisation with locations"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        # Insert organisation
        cursor.execute(
            """INSERT INTO organisations (name, description, head_user_id) 
               VALUES (%s, %s, %s) 
               RETURNING id, name, description, head_user_id""",
            (name, description, head_user_id),
        )
        result = cursor.fetchone()
        organisation_id = result["id"]  # type: ignore

        # Insert allowed municipalities
        if allowed_municipality_ids:
            for mun_id in allowed_municipality_ids:
                cursor.execute(
                    """INSERT INTO organisation_allowed_municipalities (organisation_id, municipality_id) 
                       VALUES (%s, %s)""",
                    (organisation_id, mun_id),
                )

        # Insert allowed parishes
        if allowed_parish_ids:
            for parish_id in allowed_parish_ids:
                cursor.execute(
                    """INSERT INTO organisation_allowed_parishes (organisation_id, parish_id) 
                       VALUES (%s, %s)""",
                    (organisation_id, parish_id),
                )

        # Fetch complete organisation data with locations
        cursor.execute(
            """SELECT 
                o.id, o.name, o.description, o.head_user_id,
                ARRAY_AGG(DISTINCT m.id) FILTER (WHERE m.id IS NOT NULL) as allowed_municipality_ids,
                ARRAY_AGG(DISTINCT m.name) FILTER (WHERE m.name IS NOT NULL) as allowed_municipalities,
                ARRAY_AGG(DISTINCT p.id) FILTER (WHERE p.id IS NOT NULL) as allowed_parish_ids,
                ARRAY_AGG(DISTINCT p.name) FILTER (WHERE p.name IS NOT NULL) as allowed_parishes
               FROM organisations o
               LEFT JOIN organisation_allowed_municipalities oam ON o.id = oam.organisation_id
               LEFT JOIN municipalities m ON oam.municipality_id = m.id
               LEFT JOIN organisation_allowed_parishes oap ON o.id = oap.organisation_id
               LEFT JOIN parishes p ON oap.parish_id = p.id
               WHERE o.id = %s
               GROUP BY o.id, o.name, o.description, o.head_user_id""",
            (organisation_id,),
        )
        organisation_data = cursor.fetchone()
        conn.commit()
        return organisation_data
    finally:
        cursor.close()
        conn.close()


def check_organisation_exists_by_name(name):
    """Check if an organisation with the given name exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM organisations WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def check_organisation_exists_by_id(organisation_id):
    """Check if an organisation with the given ID exists"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute("SELECT id FROM organisations WHERE id = %s", (organisation_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_organisations_from_db():
    """Get all organisations with their allowed locations"""
    conn = get_db_connection()
    cursor = get_db_cursor(conn)

    try:
        cursor.execute(
            """SELECT 
                o.id, o.name, o.description, o.head_user_id,
                ARRAY_AGG(DISTINCT m.id) FILTER (WHERE m.id IS NOT NULL) as allowed_municipality_ids,
                ARRAY_AGG(DISTINCT m.name) FILTER (WHERE m.name IS NOT NULL) as allowed_municipalities,
                ARRAY_AGG(DISTINCT p.id) FILTER (WHERE p.id IS NOT NULL) as allowed_parish_ids,
                ARRAY_AGG(DISTINCT p.name) FILTER (WHERE p.name IS NOT NULL) as allowed_parishes
               FROM organisations o
               LEFT JOIN organisation_allowed_municipalities oam ON o.id = oam.organisation_id
               LEFT JOIN municipalities m ON oam.municipality_id = m.id
               LEFT JOIN organisation_allowed_parishes oap ON o.id = oap.organisation_id
               LEFT JOIN parishes p ON oap.parish_id = p.id
               GROUP BY o.id, o.name, o.description, o.head_user_id
               ORDER BY o.id ASC"""
        )
        organisations = cursor.fetchall()
        return organisations
    finally:
        cursor.close()
        conn.close()
