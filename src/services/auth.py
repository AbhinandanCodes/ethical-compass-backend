import jwt
import datetime
from flask_bcrypt import Bcrypt
from ..db import get_db_connection
import os

bcrypt = Bcrypt()
SECRET_KEY = os.getenv("SECRET_KEY")


def register_user(username, email, password):
    """
    Create a new user in the database.

    Parameters:
        username (str) — unique username
        email (str) — unique email address
        password (str) — plain text password

    Process:
        - Hash password using bcrypt
        - Insert user into 'users' table
        - Return generated user ID

    Returns:
        dict:
            {
                "message": "User registered successfully",
                "user_id": <int>
            }

        OR

            {
                "error": "User already exists"
            }

    Security:
        Passwords are hashed before storage.
        Unique constraints enforced at database level.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (username, email, hashed_pw),
        )

        user_id = cur.fetchone()["id"] # type: ignore
        conn.commit()

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    except Exception:
        conn.rollback()
        return {"error": "User already exists"}

    finally:
        cur.close()
        conn.close()


def login_user(email, password):
    """
    Authenticate user and generate JWT token.

    Parameters:
        email (str) — user email
        password (str) — plain text password

    Process:
        - Fetch user by email
        - Compare password using bcrypt hash check
        - Generate JWT containing:
            - user_id
            - expiration (24 hours)

    Returns:
        dict:
            {
                "message": "Login successful",
                "token": "<JWT_TOKEN>"
            }

        OR

        tuple:
            ({"error": "Invalid credentials"}, 401)

    Token Payload:
        {
            "user_id": <int>,
            "exp": <timestamp>
        }

    Token Algorithm:
        HS256
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password_hash FROM users WHERE email=%s",
        (email,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return {"error": "Invalid credentials"}, 401

    if not bcrypt.check_password_hash(user["password_hash"], password): # type: ignore
        return {"error": "Invalid credentials"}, 401

    token = jwt.encode(
        {
            "user_id": user["id"], # type: ignore
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return {
        "message": "Login successful",
        "token": token
    }