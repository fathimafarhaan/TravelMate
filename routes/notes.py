"notes routes"
from flask import Blueprint, request, jsonify
import db

notes_bp = Blueprint("planning_notes", __name__)


@notes_bp.route("/trips/<int:trip_id>/planning_notes", methods=["POST"])
def create_note(trip_id):
    "function for creating a new note for a specific trip"
    data = request.get_json()
    result = db.run_query_no_output(
        """INSERT INTO planning_notes 
        (
            trip_id,
            note_text
        ) VALUES (?,?)""",
        (trip_id,
         data["note_text"]
        )
    )
    return jsonify(
    {
        "id": result["lastrowid"],
        "message": "Note created successfully",
    }
), 201


@notes_bp.route("/trips/<int:trip_id>/planning_notes", methods=["GET"])
def get_notes(trip_id):
    "function for getting all notes for a specific trip"
    return jsonify(db.run_query("SELECT * FROM planning_notes WHERE trip_id=?", (trip_id,)))


@notes_bp.route("/planning_notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    "function for updating a note by id"
    data = request.get_json()
    result = db.run_query_no_output(
        """UPDATE planning_notes SET 
            note_text=?
        WHERE id=?""",
        (data["note_text"],
         note_id
        )
    )
    if result["rowcount"] == 0:
        return jsonify({"error":"Note not found"}),404

    return jsonify({"message":"Note updated successfully"}),200


@notes_bp.route("/planning_notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    "function for deleting a note by id"
    result = db.run_query_no_output("DELETE FROM planning_notes WHERE id=?", (note_id,))
    if result["rowcount"] == 0:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"message": "Note deleted successfully"}), 200