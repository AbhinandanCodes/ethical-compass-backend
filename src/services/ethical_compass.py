import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from torch.nn import Softmax
import numpy as np
from ..config import Config


class EthicalCompass:
    """
    Multi-layer ethical evaluation system.

    Layer 1: Ethical vs Unethical classification.
    Layer 2: Emotional profile extraction.
    Layer 3: Ethical acceptability score (0 - 100).
    """

    def __init__(self):
        """Initialize all 3 evaluation layers."""

        # ---------------- Layer 1 - Ethics ----------------
        self.ETHICS_MODEL_PATH = Config.BASE_LAYERS_PATH + "layer1/model"
        self.ethics_tokenizer = AutoTokenizer.from_pretrained(self.ETHICS_MODEL_PATH)
        self.ethics_model = AutoModelForSequenceClassification.from_pretrained(
            self.ETHICS_MODEL_PATH
        )
        self.ethics_model.eval()

        # ---------------- Layer 2 - Emotions ----------------
        self.EMOTION_MODEL_PATH = Config.BASE_LAYERS_PATH + "layer2/model"
        self.emotion_tokenizer = AutoTokenizer.from_pretrained(self.EMOTION_MODEL_PATH)
        self.emotion_model = AutoModelForSequenceClassification.from_pretrained(
            self.EMOTION_MODEL_PATH
        )
        self.emotion_model.eval()

        # ---------------- Layer 3 - Moral Scoring ----------------
        self.POLICING_INDEX_MODEL_PATH = Config.BASE_LAYERS_PATH + "layer3/model"
        self.score_tokenizer = AutoTokenizer.from_pretrained(
            self.POLICING_INDEX_MODEL_PATH
        )
        self.score_model = AutoModelForSequenceClassification.from_pretrained(
            self.POLICING_INDEX_MODEL_PATH
        )
        self.policing_index_pipeline = pipeline(
            "text-classification",
            model=self.score_model,
            tokenizer=self.score_tokenizer,
            function_to_apply="none",
        )

        self.softmax = Softmax(dim=1)

    @staticmethod
    def _add_punctuation(situation: str, action: str):
        if situation[-1] != ".":
            situation += "."
        if action[-1] != ".":
            action += "."
        return (situation, action)

    def _classify_ethics(self, text: str):
        inputs = self.ethics_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=256
        )
        with torch.no_grad():
            outputs = self.ethics_model(**inputs)
            probs = self.softmax(outputs.logits).squeeze().tolist()

        pred_label = int(torch.argmax(outputs.logits, dim=1).item())
        label_name = "Unethical" if pred_label == 0 else "Ethical"

        return {
            "label": label_name,
            "scores": {
                "unethical": float(round(probs[0] * 100, 2)),
                "ethical": float(round(probs[1] * 100, 2)),
            },
        }

    def _classify_emotions(self, text: str):
        inputs = self.emotion_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=64
        )
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
            probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]

        top3_idx = np.argsort(probs)[-3:][::-1]
        top3_scores = probs[top3_idx]
        top3_labels = [Config.EMOTION_LABELS[i] for i in top3_idx]

        return [
            {"emotion": emo, "score": float(format(score * 100, ".2f"))}
            for emo, score in zip(top3_labels, top3_scores)
        ]

    def _policing_index_scoring(self, text: str):
        result = self.policing_index_pipeline(text)[0]["score"]
        final_score = 100 - max(0, min(100, result))
        return {"policing_index": float(round(final_score, 2))}

    def evaluate(self, situation: str, action: str):
        situation, action = EthicalCompass._add_punctuation(situation, action)

        layer1_text = f"Situation: {situation} Action: {action}"
        layer2_text = situation + " " + action

        ethics_result = self._classify_ethics(layer1_text)
        emotion_result = self._classify_emotions(layer2_text)
        policing_index_score = self._policing_index_scoring(action)

        return {
            "input_text": layer1_text,
            "layer1_ethics": ethics_result,
            "layer2_emotions": emotion_result,
            "layer3_policing": policing_index_score,
        }


# Global instance
ethical_compass = EthicalCompass()
