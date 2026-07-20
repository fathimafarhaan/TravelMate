"unit test for the Trips API endpoints"

import unittest

from app import app
import db


class TestTripsAPI(unittest.TestCase):
    """Unit tests for Trips API."""

    def setUp(self):
        "Set up the test client and initialize the database"
        self.client = app.test_client()

        db.run_query_no_output("DELETE FROM expenses")
        db.run_query_no_output("DELETE FROM planning_notes")
        db.run_query_no_output("DELETE FROM places_to_visit")
        db.run_query_no_output("DELETE FROM trips")

    def test_create_trip(self):
        "Test creating a new trip"
        response = self.client.post(
            "/trips",
            json={
                "destination": "Goa",
                "country": "India",
                "travel_type": "Friends",
                "estimated_budget": 25000,
                "status": "Planned",
                "rating": 5,
                "experience_notes": "Beach trip",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["message"], "Trip created successfully")

    def test_get_trips(self):
        "Test getting all trips"
        db.run_query_no_output(
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

        response = self.client.get("/trips")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["destination"], "Goa")

    def test_get_trip(self):
        "Test getting a single trip by id"
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

        trip_id = result["lastrowid"]

        response = self.client.get(f"/trips/{trip_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["destination"], "Goa")

    def test_update_trip(self):
        "Test updating a trip by id"
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

        trip_id = result["lastrowid"]

        response = self.client.put(
            f"/trips/{trip_id}",
            json={
                "destination": "Dubai",
                "country": "UAE",
                "travel_type": "Family",
                "estimated_budget": 80000,
                "status": "Completed",
                "rating": 5,
                "experience_notes": "Amazing",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Trip updated successfully")

    def test_delete_trip(self):
        "Test deleting a trip by id"
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

        trip_id = result["lastrowid"]

        response = self.client.delete(f"/trips/{trip_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["message"], "Trip deleted successfully")


if __name__ == "__main__":
    unittest.main()
