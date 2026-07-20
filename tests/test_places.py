"""Unit tests for the Places API endpoints."""

import unittest

from app import app
import db


class TestPlacesAPI(unittest.TestCase):
    """Unit tests for Places API."""

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

    def test_create_place(self):
        """Test creating a place."""
        response = self.client.post(
            f"/trips/{self.trip_id}/places_to_visit",
            json={
                "place_name": "Baga Beach",
                "visited": False,
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["message"], "Place created successfully")

    def test_get_places(self):
        """Test getting all places."""
        db.run_query_no_output(
            """
            INSERT INTO places_to_visit
            (
                trip_id,
                place_name,
                visited
            )
            VALUES (?,?,?)
            """,
            (
                self.trip_id,
                "Baga Beach",
                False,
            ),
        )

        response = self.client.get(f"/trips/{self.trip_id}/places_to_visit")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["place_name"], "Baga Beach")

    def test_update_place(self):
        """Test updating a place."""
        result = db.run_query_no_output(
            """
            INSERT INTO places_to_visit
            (
                trip_id,
                place_name,
                visited
            )
            VALUES (?,?,?)
            """,
            (
                self.trip_id,
                "Baga Beach",
                False,
            ),
        )

        place_id = result["lastrowid"]

        response = self.client.put(
            f"/places_to_visit/{place_id}",
            json={
                "place_name": "Calangute Beach",
                "visited": True,
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Place updated successfully")

    def test_delete_place(self):
        """Test deleting a place."""
        result = db.run_query_no_output(
            """
            INSERT INTO places_to_visit
            (
                trip_id,
                place_name,
                visited
            )
            VALUES (?,?,?)
            """,
            (
                self.trip_id,
                "Baga Beach",
                False,
            ),
        )

        place_id = result["lastrowid"]

        response = self.client.delete(f"/places_to_visit/{place_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Place deleted successfully")


if __name__ == "__main__":
    unittest.main()
