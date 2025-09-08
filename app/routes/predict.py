from flask import Blueprint, request, jsonify
from app.services.combined_inference import ethics_pipeline

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict

    Run an ethics prediction on a given text scenario.  
    Returns a continuous ethics score, probability, and a categorical label.

    Request JSON:
        {
            "text": "Your moral/ethical scenario"
        }

    Response JSON:
        {
            "ethics_score": float,           # Continuous score in [-1, 1]
            "probability_ethical": float,    # Probability in [0, 1]
            "label": str                     # One of: "Unethical", "Neutral / Ambiguous", "Ethical"
        }
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"]
    result = ethics_pipeline.predict(text)
    return jsonify(result)
