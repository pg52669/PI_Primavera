"""
Database connection utilities
"""

import os
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """Create a database connection"""
    return connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "events_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def get_db_cursor(conn, dict_cursor=True):
    """Get a database cursor"""
    if dict_cursor:
        return conn.cursor(cursor_factory=RealDictCursor)
    return conn.cursor()
