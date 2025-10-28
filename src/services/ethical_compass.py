import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn import Softmax
import numpy as np
from ..config import Config


class EthicalCompass:
    """
    A two-layer ethical and emotional evaluation system.

    Layer 1: Evaluates whether a situation-action pair is ethical or unethical.
    Layer 2: Analyzes the emotional undertones present in the text.

    Attributes:
        ETHICS_MODEL_PATH (str): Path to the ethics classification model (layer1).
        EMOTION_MODEL_PATH (str): Path to the emotion classification model (layer2).
        ethics_tokenizer (AutoTokenizer): Tokenizer for ethics model.
        ethics_model (AutoModelForSequenceClassification): Pretrained ethics model.
        emotion_tokenizer (AutoTokenizer): Tokenizer for emotion model.
        emotion_model (AutoModelForSequenceClassification): Pretrained emotion model.
        softmax (Softmax): Softmax layer for probability conversion.
    """

    def __init__(self):
        """Initialize both the ethics and emotion models from pretrained weights."""
        # Load ethics model (layer 1)
        self.ETHICS_MODEL_PATH = Config.BASE_LAYERS_PATH + "layer1/model"
        self.ethics_tokenizer = AutoTokenizer.from_pretrained(self.ETHICS_MODEL_PATH)
        self.ethics_model = AutoModelForSequenceClassification.from_pretrained(self.ETHICS_MODEL_PATH)
        self.ethics_model.eval()

        # Load emotion model (layer 2)
        self.EMOTION_MODEL_PATH = Config.BASE_LAYERS_PATH + "layer2/model"
        self.emotion_tokenizer = AutoTokenizer.from_pretrained(self.EMOTION_MODEL_PATH)
        self.emotion_model = AutoModelForSequenceClassification.from_pretrained(self.EMOTION_MODEL_PATH)
        self.emotion_model.eval()

        self.softmax = Softmax(dim=1)
    
    @staticmethod
    def _add_punctuation(situation: str, action: str):
        """
        Ensure that both `situation` and `action` end with a period.

        Args:
            situation (str): The given situation text.
            action (str): The given action text.

        Returns:
            tuple: The (situation, action) with punctuation ensured.
        """
        situation = situation + "." if situation[-1] != "." else situation
        action = action + "." if action[-1] != "." else action
        return (situation, action)
    
    @staticmethod
    def _process_output(ethics_result, emotion_result):
        """
        Format the raw outputs of both layers into human-readable strings.

        Args:
            ethics_result (dict): Output from `_classify_ethics` method.
            emotion_result (list): Output from `_classify_emotions` method.

        Returns:
            tuple: Formatted strings for layer1 (ethics) and layer2 (emotions).
        """
        layer1_output = (
            f"Label: {ethics_result['label']}, "
            f"Ethical: {ethics_result['ethical_%']}% "
            f"Unethical: {ethics_result['unethical_%']}%"
        )

        emotion_result_str = ""
        for emo, score in emotion_result:
            emotion_result_str += f"{score:.2f}% {emo} "
        layer2_output = f"{emotion_result_str}"

        return (layer1_output, layer2_output)
    

    def _classify_ethics(self, text: str):
        """
        Predict whether the given text is ethical or unethical.

        Args:
            text (str): Input text combining situation and action.

        Returns:
            dict: A dictionary with label, ethical%, and unethical% scores.
        """
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
            "unethical_%": round(probs[0] * 100, 2),
            "ethical_%": round(probs[1] * 100, 2),
        }


    def _classify_emotions(self, text: str):
        """
        Predict the top-3 emotions expressed in the text.

        Args:
            text (str): Input text to analyze emotions from.

        Returns:
            list[tuple]: List of top-3 (emotion_label, probability%) pairs.
        """
        inputs = self.emotion_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=64
        )

        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
            probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]

        top3_idx = np.argsort(probs)[-3:][::-1]
        top3_scores = probs[top3_idx]
        top3_labels = [Config.EMOTION_LABELS[i] for i in top3_idx]

        return list(zip(top3_labels, top3_scores * 100))
    
    def evaluate(self, situation: str, action: str):
        """
        Evaluate the ethics and emotional tone of a situation-action pair.

        This method combines both models:
        - Layer 1 determines ethical/unethical classification.
        - Layer 2 identifies dominant emotional tones.

        Args:
            situation (str): Description of the situation.
            action (str): The action taken within that situation.

        Returns:
            dict: Combined structured output from both layers.
        """
        situation, action = EthicalCompass._add_punctuation(situation, action)
        layer1_text = f"Situation: {situation} Action: {action}"
        layer2_text = situation + "" + action

        ethics_result = self._classify_ethics(layer1_text)
        emotion_result = self._classify_emotions(layer2_text)
        layer1_output, layer2_output = EthicalCompass._process_output(
            ethics_result, emotion_result
        )

        return {
            "text": layer1_text,
            "layer1": layer1_output,
            "layer2": layer2_output,
        }


# Create a global instance for convenience
ethical_compass = EthicalCompass()
