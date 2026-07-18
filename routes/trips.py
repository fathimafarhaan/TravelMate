"""trip routes"""

from flask import Blueprint, request, jsonify
import db

trips_bp = Blueprint("trips", __name__)


@trips_bp.route("/trips", methods=["POST"])
def create_trips():
    "function for creating a new trip"
    data = request.get_json()
    new_id = db.run_query_no_output(
        """INSERT INTO trips 
        (
            destination,
            country,
            travel_type,
            estimated_budget,
            status,
            rating,
            experience_notes
        ) VALUES (?,?,?,?,?,?,?)""",
        (
            data["destination"],
            data["country"],
            data["travel_type"],
            data["estimated_budget"],
            data.get("status", "Planned"),
            data.get("rating", None),
            data.get("experience_notes", None),
        ),
    )
    return jsonify({"id": new_id}), 201


@trips_bp.route("/trips", methods=["GET"])
def get_trips():
    "function for getting all trips"
    return jsonify(db.run_query("SELECT * FROM trips"))


@trips_bp.route("/trips/<int:trip_id>", methods=["GET"])
def get_trip(trip_id):
    "function for getting a single trip by id"
    trips = db.run_query_one("SELECT * FROM trips WHERE id=?", (trip_id,))
    if trips is None:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify(trips)


@trips_bp.route("/trips/<int:trip_id>", methods=["PUT"])
def update_trip(trip_id):
    "function for updating a trip by id"
    data = request.get_json()
    rows_updated = db.run_query_no_output(
        """UPDATE trips SET 
            destination=?, 
            country=?, 
            travel_type=?, 
            estimated_budget=?, 
            status=?, 
            rating=?, 
            experience_notes=?
        WHERE id=?""",
        (
            data["destination"],
            data["country"],
            data["travel_type"],
            data["estimated_budget"],
            data.get("status", "Planned"),
            data.get("rating", None),
            data.get("experience_notes", None),
            trip_id,
        ),
    )
    if rows_updated == 0:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({"message": "Trip updated"}), 200


@trips_bp.route("/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    "function for deleting a trip by id"
    rows_deleted = db.run_query_no_output("DELETE FROM trips WHERE id=?", (trip_id,))
    if rows_deleted == 0:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({"message": "Trip deleted"}), 200