import jwt
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY")


def token_required(f):
    """
    Decorator to protect routes using JWT authentication.

    Expects:
        Authorization header in the format:
            Authorization: Bearer <JWT_TOKEN>

    Behavior:
        - Verifies token presence
        - Validates token signature
        - Checks expiration
        - Extracts user_id from token payload
        - Attaches user_id to request context as:
              request.user_id

    Returns:
        401 JSON response if:
            - Token missing
            - Token malformed
            - Token expired
            - Token invalid

    Usage:
        @app.route("/protected")
        @token_required
        def protected_route():
            user_id = request.user_id
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            # Expect: Authorization: Bearer <token>
            parts = auth_header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Invalid token format"}), 401

            token = parts[1]

            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user_id = decoded["user_id"] # type: ignore

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated