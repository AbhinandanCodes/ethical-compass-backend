from flask import Blueprint, request, jsonify
from ..services import auth as auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Handle user registration.

    Endpoint:
        POST /auth/register

    Expects JSON body:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }

    Behavior:
        - Validates required fields
        - Hashes password securely
        - Stores user in database
        - Enforces unique username and email

    Success Response:
        {
            "message": "User registered successfully",
            "user_id": <int>
        }

    Error Responses:
        400 — Missing required fields
        200 — {"error": "User already exists"}

    Notes:
        Passwords are never stored in plain text.
        They are hashed using bcrypt.
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400

    result = auth_service.register_user(
        data["username"],
        data["email"],
        data["password"]
    )

    return jsonify(result)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Handle user authentication.

    Endpoint:
        POST /auth/login

    Expects JSON body:
        {
            "email": "string",
            "password": "string"
        }

    Behavior:
        - Verifies email exists
        - Validates password against stored hash
        - Generates JWT token valid for 24 hours

    Success Response:
        {
            "message": "Login successful",
            "token": "<JWT_TOKEN>"
        }

    Error Responses:
        400 — Missing email or password
        401 — Invalid credentials

    Notes:
        The returned token must be included in protected requests as:

            Authorization: Bearer <JWT_TOKEN>
    """
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    result = auth_service.login_user(
        data["email"],
        data["password"]
    )

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result)