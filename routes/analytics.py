"""Analytics routes"""

from flask import Blueprint, jsonify
from analytics import get_dashboard_data

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    """Return dashboard analytics"""
    return jsonify(get_dashboard_data())