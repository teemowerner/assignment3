from flask import Blueprint, jsonify

bp = Blueprint("applications", __name__)

@bp.route("/", methods=["POST"])
def apply():
    return jsonify({"message": "Application submitted"})
