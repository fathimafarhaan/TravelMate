"""unit testing for database functions"""
import unittest
import sqlite3

import db


class TestDatabase(unittest.TestCase):
    """Unit tests for database functions."""

    def test_get_connection(self):
        """Test that a database connection is created"""
        connection = db.get_connection()

        self.assertIsInstance(connection, sqlite3.Connection)

        connection.close()

    def test_init_db(self):
        """Test that database tables are created"""

        db.init_db()

        connection = db.get_connection()

        tables = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """).fetchall()

        table_names = [table["name"] for table in tables]

        self.assertIn("trips", table_names)
        self.assertIn("places_to_visit", table_names)
        self.assertIn("planning_notes", table_names)
        self.assertIn("expenses", table_names)

        connection.close()

    def test_run_query(self):
        """Test SELECT query returning multiple rows"""

        result = db.run_query("SELECT * FROM trips")

        self.assertIsInstance(result, list)

    def test_run_query_one(self):
        """Test SELECT query returning one row"""

        result = db.run_query_one("SELECT * FROM trips WHERE id=?", (999,))

        self.assertIsNone(result)

    def test_run_query_no_output(self):
        """Test INSERT query execution"""

        result = db.run_query_no_output(
            """
            INSERT INTO trips
            (
                destination,
                country,
                travel_type,
                estimated_budget,
                status
            )
            VALUES (?,?,?,?,?)
            """,
            ("Goa", "India", "Friends", 25000, "Planned"),
        )

        self.assertIn("lastrowid", result)
        self.assertIn("rowcount", result)
        self.assertEqual(result["rowcount"], 1)


if __name__ == "__main__":
    unittest.main()
