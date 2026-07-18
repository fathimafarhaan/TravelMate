"""
Analytics functions using pandas
"""

import pandas as pd
import db


def get_trips_df():
    """Return trips dataframe"""
    trips = db.run_query("SELECT * FROM trips")
    return pd.DataFrame(
        trips,
        columns=[
            "id",
            "destination",
            "country",
            "travel_type",
            "estimated_budget",
            "status",
            "rating",
            "experience_notes",
            "created_at",
        ],
    )


def get_expenses_df():
    """Return expenses dataframe"""
    expenses = db.run_query("SELECT * FROM expenses")
    return pd.DataFrame(
        expenses,
        columns=[
            "id",
            "trip_id",
            "category",
            "amount",
            "description",
            "expense_date",
        ],
    )


def get_places_df():
    """Return places dataframe"""
    places = db.run_query("SELECT * FROM places_to_visit")
    return pd.DataFrame(
        places,
        columns=[
            "id",
            "trip_id",
            "place_name",
            "visited",
        ],
    )


def get_trip_summary(trips_df):
    """Trip statistics"""

    if trips_df.empty:
        return {
            "total_trips": 0,
            "completed_trips": 0,
            "planned_trips": 0,
            "completion_rate": 0,
            "average_budget": 0,
            "average_rating": None,
        }

    total = len(trips_df)
    completed = int((trips_df["status"] == "Completed").sum())

    return {
        "total_trips": total,
        "completed_trips": completed,
        "planned_trips": int((trips_df["status"] == "Planned").sum()),
        "completion_rate": round(completed * 100 / total, 2),
        "average_budget": round(
            float(trips_df["estimated_budget"].mean()), 2
        ),
        "average_rating": (
            round(float(trips_df["rating"].dropna().mean()), 2)
            if trips_df["rating"].notna().any()
            else None
        ),
    }


def get_travel_type_summary(trips_df):
    """Trips by travel type"""

    if trips_df.empty:
        return []

    return (
        trips_df.groupby("travel_type")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )


def get_country_summary(trips_df):
    """Trips by country"""

    if trips_df.empty:
        return []

    return (
        trips_df.groupby("country")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )


def get_expense_summary(expenses_df):
    """Expense by category"""

    if expenses_df.empty:
        return {
            "total_expense": 0,
            "expense_summary": [],
        }

    return {
        "total_expense": round(float(expenses_df["amount"].sum()), 2),
        "expense_summary": (
            expenses_df.groupby("category")["amount"]
            .sum()
            .reset_index(name="total_amount")
            .to_dict(orient="records")
        ),
    }


def get_monthly_trend(trips_df):
    """Trips created every month"""

    if trips_df.empty:
        return []

    trips_df["created_at"] = pd.to_datetime(trips_df["created_at"])

    return (
        trips_df.groupby(trips_df["created_at"].dt.strftime("%Y-%m"))
        .size()
        .reset_index(name="trip_count")
        .rename(columns={"created_at": "month"})
        .to_dict(orient="records")
    )


def get_budget_vs_expense(trips_df, expenses_df):
    """Budget vs actual expense"""

    if trips_df.empty or expenses_df.empty:
        return []

    expense = (
        expenses_df.groupby("trip_id")["amount"]
        .sum()
        .reset_index(name="actual_expense")
    )

    merged = trips_df.merge(
        expense,
        left_on="id",
        right_on="trip_id",
        how="left",
    )

    merged["actual_expense"] = merged["actual_expense"].fillna(0)

    return (
        merged[
            [
                "destination",
                "estimated_budget",
                "actual_expense",
            ]
        ]
        .rename(
            columns={
                "estimated_budget": "budget",
            }
        )
        .to_dict(orient="records")
    )


def get_places_summary(places_df):
    """Visited vs pending places"""

    if places_df.empty:
        return {
            "visited": 0,
            "pending": 0,
        }

    visited = int((places_df["visited"] == 1).sum())

    return {
        "visited": visited,
        "pending": len(places_df) - visited,
    }


def get_dashboard_data():
    """Return complete dashboard"""

    trips_df = get_trips_df()
    expenses_df = get_expenses_df()
    places_df = get_places_df()

    dashboard = {}

    dashboard.update(get_trip_summary(trips_df))
    dashboard.update(get_expense_summary(expenses_df))

    dashboard["travel_type_summary"] = get_travel_type_summary(trips_df)
    dashboard["country_summary"] = get_country_summary(trips_df)
    dashboard["monthly_trend"] = get_monthly_trend(trips_df)
    dashboard["budget_vs_expense"] = get_budget_vs_expense(
        trips_df,
        expenses_df,
    )
    dashboard["places_summary"] = get_places_summary(places_df)

    return dashboard