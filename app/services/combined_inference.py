import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.config import Config
from typing import Optional

class EthicsPipeline:
    """
    Ethics Inference Pipeline (Regression only).

    Loads a regression model (DeBERTa) to output a continuous ethics score
    and maps it into a probability.
    """

    def __init__(self, device: Optional[str] = None):
        """
        Initialize the EthicsPipeline with model path from Config.

        Args:
            device (str, optional): Device to run the model on.
                                    Defaults to "cuda" if available, else "cpu".
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load regression model
        self.tokenizer_pred = AutoTokenizer.from_pretrained(Config.ETHICS_PREDICTION_MODEL)
        self.model_pred = AutoModelForSequenceClassification.from_pretrained(
            Config.ETHICS_PREDICTION_MODEL,
            num_labels=1
        )
        self.model_pred.to(self.device)
        self.model_pred.eval()

    def predict(self, text: str) -> dict:
        """
        Predict the ethics score for a given text.

        Args:
            text (str): The moral/ethical scenario.

        Returns:
            dict: {
                "ethics_score": float,           # Continuous score [-1,1]
                "probability_ethical": float,    # Probability [0,1]
                "label": str                     # Human-readable label
            }
        """
        inputs_pred = self.tokenizer_pred(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            raw_score = self.model_pred(**inputs_pred).logits.squeeze().item()

        # Clamp score safely into [-1, 1]
        score = max(min(raw_score, 1.0), -1.0)

        # Map score to probability [0,1]
        prob_ethical = (score + 1) / 2.0

        # Human-readable label
        if score <= -0.15:
            label = "Unethical"
        elif score >= 0.15:
            label = "Ethical"
        else:
            label = "Neutral / Ambiguous"

        return {
            "ethics_score": round(score, 3),
            "probability_ethical": round(prob_ethical, 3),
            "label": label
        }


# Singleton instance
ethics_pipeline = EthicsPipeline()
