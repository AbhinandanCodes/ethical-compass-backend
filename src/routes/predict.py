from flask import Blueprint, request, jsonify
from ..services import ethical_compass

# Define a Flask Blueprint for prediction-related routes
predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    """
    Handle POST requests to the /predict endpoint.

    Expects a JSON body with the following fields:
        {
            "situation": "string",
            "action": "string"
        }

    Runs the EthicalCompass model to evaluate:
        - Ethical classification (Ethical / Unethical)
        - Emotional tone (Top-3 emotions)

    Returns:
        JSON response containing:
            {
                "text": <combined input>,
                "layer1": <ethics result>,
                "layer2": <emotion result>
            }

    Example Request:
        POST /predict
        {
            "situation": "You find a lost wallet on the street",
            "action": "You return it to the owner"
        }

    Example Response:
        {
            "text": "Situation: You find a lost wallet on the street. Action: You return it to the owner.",
            "layer1": "Label: Ethical Ethical: 96.2% Unethical: 3.8%",
            "layer2": "Joy 82.1% Trust 71.4% Surprise 45.9%"
        }

    Error Codes:
        400 — Missing required fields.
    """
    # Parse JSON request body
    data = request.get_json()

    # Validate input fields
    if not data or "situation" not in data or "action" not in data:
        return jsonify({"error": "Missing 'situation' or 'action' field"}), 400

    # Run ethical + emotional evaluation
    result = ethical_compass.evaluate(data["situation"], data["action"])

    # Return JSON response
    return jsonify(result)
