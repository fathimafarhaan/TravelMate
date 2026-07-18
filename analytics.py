"""Analytics functions using pandas"""

import pandas as pd
import db


def get_dashboard_data():
    """Return dashboard analytics"""

    trips = db.run_query("SELECT * FROM trips")
    expenses = db.run_query("SELECT * FROM expenses")

    trips_df = pd.DataFrame(trips)
    expenses_df = pd.DataFrame(expenses)

    analytics = {}

    

    analytics["total_trips"] = len(trips_df)

    if not trips_df.empty:

        analytics["completed_trips"] = int(
            (trips_df["status"] == "Completed").sum()
        )

        analytics["planned_trips"] = int(
            (trips_df["status"] == "Planned").sum()
        )

        analytics["average_budget"] = round(
            float(trips_df["estimated_budget"].mean()), 2
        )

        analytics["average_rating"] = round(
            float(trips_df["rating"].dropna().mean()), 2
        ) if trips_df["rating"].notna().any() else None

        analytics["travel_type_summary"] = (
            trips_df.groupby("travel_type")
            .size()
            .reset_index(name="count")
            .to_dict(orient="records")
        )

        analytics["country_summary"] = (
            trips_df.groupby("country")
            .size()
            .reset_index(name="count")
            .to_dict(orient="records")
        )

    else:

        analytics["completed_trips"] = 0
        analytics["planned_trips"] = 0
        analytics["average_budget"] = 0
        analytics["average_rating"] = None
        analytics["travel_type_summary"] = []
        analytics["country_summary"] = []

    

    if not expenses_df.empty:

        analytics["total_expense"] = round(
            float(expenses_df["amount"].sum()), 2
        )

        analytics["expense_summary"] = (
            expenses_df.groupby("category")["amount"]
            .sum()
            .reset_index(name="total_amount")
            .to_dict(orient="records")
        )

    else:

        analytics["total_expense"] = 0
        analytics["expense_summary"] = []

    return analytics