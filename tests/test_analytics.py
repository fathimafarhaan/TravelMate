"""Unit tests for analytics functions."""

import unittest

import db
from analytics import (
    get_trips_df,
    get_expenses_df,
    get_places_df,
    get_trip_summary,
    get_travel_type_summary,
    get_country_summary,
    get_expense_summary,
    get_monthly_trend,
    get_budget_vs_expense,
    get_places_summary,
    get_dashboard_data,
)


class TestAnalytics(unittest.TestCase):
    """Unit tests for analytics."""

    def setUp(self):
        """Prepare test data."""

        db.run_query_no_output("DELETE FROM expenses")
        db.run_query_no_output("DELETE FROM planning_notes")
        db.run_query_no_output("DELETE FROM places_to_visit")
        db.run_query_no_output("DELETE FROM trips")

        trip = db.run_query_no_output(
            """
            INSERT INTO trips
            (
                destination,
                country,
                travel_type,
                estimated_budget,
                status,
                rating
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                "Goa",
                "India",
                "Friends",
                25000,
                "Completed",
                5,
            ),
        )

        self.trip_id = trip["lastrowid"]

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
                1,
            ),
        )

    def test_trip_summary(self):
        """Test trip summary."""
        summary = get_trip_summary(get_trips_df())

        self.assertEqual(summary["total_trips"], 1)
        self.assertEqual(summary["completed_trips"], 1)

    def test_travel_type_summary(self):
        """Test travel type summary."""
        summary = get_travel_type_summary(get_trips_df())

        self.assertEqual(summary[0]["travel_type"], "Friends")

    def test_country_summary(self):
        """Test country summary."""
        summary = get_country_summary(get_trips_df())

        self.assertEqual(summary[0]["country"], "India")

    def test_expense_summary(self):
        """Test expense summary."""
        summary = get_expense_summary(get_expenses_df())

        self.assertEqual(summary["total_expense"], 1500)

    def test_monthly_trend(self):
        """Test monthly trend."""
        trend = get_monthly_trend(get_trips_df())

        self.assertEqual(len(trend), 1)

    def test_budget_vs_expense(self):
        """Test budget versus expense."""
        result = get_budget_vs_expense(
            get_trips_df(),
            get_expenses_df(),
        )

        self.assertEqual(result[0]["budget"], 25000)
        self.assertEqual(result[0]["actual_expense"], 1500)

    def test_places_summary(self):
        """Test places summary."""
        summary = get_places_summary(get_places_df())

        self.assertEqual(summary["visited"], 1)
        self.assertEqual(summary["pending"], 0)

    def test_dashboard_data(self):
        """Test complete dashboard."""
        dashboard = get_dashboard_data()

        self.assertIn("total_trips", dashboard)
        self.assertIn("expense_summary", dashboard)
        self.assertIn("travel_type_summary", dashboard)
        self.assertIn("country_summary", dashboard)
        self.assertIn("monthly_trend", dashboard)
        self.assertIn("budget_vs_expense", dashboard)
        self.assertIn("places_summary", dashboard)


if __name__ == "__main__":
    unittest.main()
