"database logic"

import sqlite3
from config import DB_PATH


def get_connection():
    "function for getting a connection to the database"
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    "function for initializing the database with the schema"
    with open("schema.sql", "r", encoding="utf-8") as f:
        schema = f.read()

    with get_connection() as conn:
        conn.executescript(schema)
        conn.commit()


def run_query(query, params=()):
    "function for running a query and returning the results as a list of dictionaries"
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def run_query_one(query, params=()):
    "function for running a query and returning a single result as a dictionary"
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def run_query_no_output(query, params=()):
    "function for running a query that does not return any output"
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount
        }