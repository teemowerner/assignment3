from flask import Blueprint, jsonify

# Blueprint 정의
bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    return jsonify({"message": "User registered successfully"})

@bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "User logged in successfully"})
