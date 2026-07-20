"expenses routes"

from flask import Blueprint, request, jsonify
import db

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.route("/trips/<int:trip_id>/expenses", methods=["POST"])
def create_expense(trip_id):
    "function for creating a new expense for a specific trip"
    data = request.get_json()
    result = db.run_query_no_output(
        """INSERT INTO expenses 
        (
            trip_id,
            category,
            amount,
            description,
            expense_date
        ) VALUES (?,?,?,?,?)""",
        (
            trip_id,
            data["category"],
            data["amount"],
            data["description"],
            data["expense_date"],
        ),
    )
    return (
        jsonify(
            {
                "id": result["lastrowid"],
                "message": "Expense created successfully",
            }
        ),
        201,
    )


@expenses_bp.route("/trips/<int:trip_id>/expenses", methods=["GET"])
def get_expenses(trip_id):
    "function for getting all expenses for a specific trip"
    return jsonify(db.run_query("SELECT * FROM expenses WHERE trip_id=?", (trip_id,)))


@expenses_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    "function for updating an expense by id"
    data = request.get_json()
    result = db.run_query_no_output(
        """UPDATE expenses SET 
            category=?, 
            amount=?,
            description=?,
            expense_date=?
        WHERE id=?""",
        (
            data["category"],
            data["amount"],
            data["description"],
            data["expense_date"],
            expense_id,
        ),
    )
    if result["rowcount"] == 0:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({"message": "Expense updated successfully"}), 200


@expenses_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    "function for deleting an expense by id"
    result = db.run_query_no_output("DELETE FROM expenses WHERE id=?", (expense_id,))
    if result["rowcount"] == 0:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify({"message": "Expense deleted successfully"}), 200
