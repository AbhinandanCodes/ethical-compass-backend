import os

class Config:
    PROJECT_NAME = "Ethics Classifier API"
    ETHICS_PREDICTION_MODEL = os.path.join(os.path.dirname(__file__), "../","ml_models/ethics_prediction_deberta_v3_small")
