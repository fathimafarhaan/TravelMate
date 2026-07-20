"""Unit tests for the Expenses API endpoints."""

import unittest

from app import app
import db


class TestExpensesAPI(unittest.TestCase):
    """Unit tests for Expenses API."""

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

    def test_create_expense(self):
        """Test creating an expense."""
        response = self.client.post(
            f"/trips/{self.trip_id}/expenses",
            json={
                "category": "Food",
                "amount": 1500,
                "description": "Dinner",
                "expense_date": "2026-07-18",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["message"], "Expense created successfully")

    def test_get_expenses(self):
        """Test getting all expenses."""
        db.run_query_no_output(
            """
            INSERT INTO expenses
            (
                trip_id,
                category,
                amount,
                description,
                expense_date
            )
            VALUES (?,?,?,?,?)
            """,
            (
                self.trip_id,
                "Food",
                1500,
                "Dinner",
                "2026-07-18",
            ),
        )

        response = self.client.get(f"/trips/{self.trip_id}/expenses")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Food")

    def test_update_expense(self):
        """Test updating an expense."""
        result = db.run_query_no_output(
            """
            INSERT INTO expenses
            (
                trip_id,
                category,
                amount,
                description,
                expense_date
            )
            VALUES (?,?,?,?,?)
            """,
            (
                self.trip_id,
                "Food",
                1500,
                "Dinner",
                "2026-07-18",
            ),
        )

        expense_id = result["lastrowid"]

        response = self.client.put(
            f"/expenses/{expense_id}",
            json={
                "category": "Hotel",
                "amount": 5000,
                "description": "Resort Stay",
                "expense_date": "2026-07-19",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Expense updated successfully",
        )

    def test_delete_expense(self):
        """Test deleting an expense."""
        result = db.run_query_no_output(
            """
            INSERT INTO expenses
            (
                trip_id,
                category,
                amount,
                description,
                expense_date
            )
            VALUES (?,?,?,?,?)
            """,
            (
                self.trip_id,
                "Food",
                1500,
                "Dinner",
                "2026-07-18",
            ),
        )

        expense_id = result["lastrowid"]

        response = self.client.delete(f"/expenses/{expense_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Expense deleted successfully",
        )


if __name__ == "__main__":
    unittest.main()
