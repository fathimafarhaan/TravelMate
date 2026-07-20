"places routes"

from flask import Blueprint, request, jsonify
import db

places_bp = Blueprint("places_to_visit", __name__)


@places_bp.route("/trips/<int:trip_id>/places_to_visit", methods=["POST"])
def create_place(trip_id):
    "function for creating a new place for a specific trip"
    data = request.get_json()
    result = db.run_query_no_output(
        """INSERT INTO places_to_visit 
        (
            trip_id,
            place_name,
            visited
        ) VALUES (?,?,?)""",
        (trip_id, data["place_name"], data.get("visited", False)),
    )
    return (
        jsonify(
            {
                "id": result["lastrowid"],
                "message": "Place created successfully",
            }
        ),
        201,
    )


@places_bp.route("/trips/<int:trip_id>/places_to_visit", methods=["GET"])
def get_places(trip_id):
    "function for getting all places for a specific trip"
    return jsonify(
        db.run_query("SELECT * FROM places_to_visit WHERE trip_id=?", (trip_id,))
    )


@places_bp.route("/places_to_visit/<int:place_id>", methods=["PUT"])
def update_place(place_id):
    "function for updating a place by id"
    data = request.get_json()
    result = db.run_query_no_output(
        """UPDATE places_to_visit SET 
            place_name=?, 
            visited=?
        WHERE id=?""",
        (data["place_name"], data.get("visited", False), place_id),
    )
    if result["rowcount"] == 0:
        return jsonify({"error": "Place not found"}), 404

    return jsonify({"message": "Place updated successfully"}), 200


@places_bp.route("/places_to_visit/<int:place_id>", methods=["DELETE"])
def delete_place(place_id):
    "function for deleting a place by id"
    result = db.run_query_no_output(
        "DELETE FROM places_to_visit WHERE id=?", (place_id,)
    )
    if result["rowcount"] == 0:
        return jsonify({"error": "Place not found"}), 404
    return jsonify({"message": "Place deleted successfully"}), 200
