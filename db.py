
"database logic"

import sqlite3
import mysql.connector

from config import (
    DB_TYPE,
    DB_PATH,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)


def get_connection():
    """Return a database connection."""

    if DB_TYPE == "sqlite":

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_db():
    """Initialize database."""

    if DB_TYPE == "sqlite":

        with open(
            "schema.sql",
            "r",
            encoding="utf-8"
        ) as f:

            schema = f.read()

        conn = get_connection()

        conn.executescript(schema)

        conn.commit()

        conn.close()

    else:

        with open(
            "schema_mysql.sql",
            "r",
            encoding="utf-8"
        ) as f:

            schema = f.read()

        conn = get_connection()

        cursor = conn.cursor()

        for statement in schema.split(";"):

            statement = statement.strip()

            if statement:

                cursor.execute(statement)

        conn.commit()

        cursor.close()

        conn.close()


def run_query(query, params=()):
    """Run a SELECT query and return all rows."""

    conn = get_connection()

    if DB_TYPE == "mysql":
        query = query.replace("?", "%s")

    if DB_TYPE == "sqlite":

        rows = conn.execute(query, params).fetchall()
        conn.close()

        return [dict(row) for row in rows]

    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, params)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

    

def run_query_one(query, params=()):
    """Run a SELECT query and return one row."""

    conn = get_connection()

    if DB_TYPE == "mysql":
        query = query.replace("?", "%s")

    if DB_TYPE == "sqlite":

        row = conn.execute(query, params).fetchone()
        conn.close()

        return dict(row) if row else None

    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, params)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row



def run_query_no_output(query, params=()):
    """Run INSERT, UPDATE or DELETE queries."""

    conn = get_connection()

    if DB_TYPE == "mysql":
        query = query.replace("?", "%s")

    if DB_TYPE == "sqlite":

        cursor = conn.execute(query, params)
        conn.commit()

        result = {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount,
        }

        conn.close()

        return result

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    result = {
        "lastrowid": cursor.lastrowid,
        "rowcount": cursor.rowcount,
    }

    cursor.close()
    conn.close()

    return result