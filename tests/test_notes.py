"""Unit tests for the Notes API endpoints."""

import unittest

from app import app
import db


class TestNotesAPI(unittest.TestCase):
    """Unit tests for Notes API."""

    def setUp(self):
        """Set up the test client and clean the database."""
        self.client = app.test_client()

        db.run_query_no_output("DELETE FROM expenses")
        db.run_query_no_output("DELETE FROM planning_notes")
        db.run_query_no_output("DELETE FROM places_to_visit")
        db.run_query_no_output("DELETE FROM trips")

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
            (
                "Goa",
                "India",
                "Friends",
                25000,
                "Planned",
            ),
        )

        self.trip_id = result["lastrowid"]

    def test_create_note(self):
        """Test creating a note."""
        response = self.client.post(
            f"/trips/{self.trip_id}/planning_notes",
            json={
                "note_text": "Book flight tickets",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["message"], "Note created successfully")

    def test_get_notes(self):
        """Test getting all notes."""
        db.run_query_no_output(
            """
            INSERT INTO planning_notes
            (
                trip_id,
                note_text
            )
            VALUES (?,?)
            """,
            (
                self.trip_id,
                "Book flight tickets",
            ),
        )

        response = self.client.get(f"/trips/{self.trip_id}/planning_notes")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["note_text"], "Book flight tickets")

    def test_update_note(self):
        """Test updating a note."""
        result = db.run_query_no_output(
            """
            INSERT INTO planning_notes
            (
                trip_id,
                note_text
            )
            VALUES (?,?)
            """,
            (
                self.trip_id,
                "Book flight tickets",
            ),
        )

        note_id = result["lastrowid"]

        response = self.client.put(
            f"/planning_notes/{note_id}",
            json={
                "note_text": "Book hotel also",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Note updated successfully")

    def test_delete_note(self):
        """Test deleting a note."""
        result = db.run_query_no_output(
            """
            INSERT INTO planning_notes
            (
                trip_id,
                note_text
            )
            VALUES (?,?)
            """,
            (
                self.trip_id,
                "Book flight tickets",
            ),
        )

        note_id = result["lastrowid"]

        response = self.client.delete(f"/planning_notes/{note_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Note deleted successfully")


if __name__ == "__main__":
    unittest.main()
