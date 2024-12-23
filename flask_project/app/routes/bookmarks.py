from flask import Blueprint, jsonify

bp = Blueprint("bookmarks", __name__)

@bp.route("/", methods=["GET"])
def list_bookmarks():
    return jsonify({"bookmarks": []})
