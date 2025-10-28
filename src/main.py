
"""
main.py

Entry point for the Ethics Classifier API Flask application.

This module creates and runs the Flask app, registering all routes
and providing a root endpoint to verify the server is running.
"""

from flask import Flask, jsonify
from .routes import predict_bp
from.config import Config

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance with registered routes.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register API routes
    app.register_blueprint(predict_bp)

    @app.route("/")
    def root():
        """
        Root endpoint to check if the API is running.

        Returns:
            JSON: A simple message indicating the server is live.
        """
        return jsonify({"message": f"{Config.PROJECT_NAME} is running"})

    return app

def main():
    app = create_app()
    print("Server running...")
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == "__main__":
    main()