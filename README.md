# Ethical Compass 🧭

A lightweight ethics evaluation API that predicts whether a given scenario is **Ethical**, **Unethical**, or **Neutral / Ambiguous**, along with a continuous ethics score and probability.

---

## 🚀 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/AbhinandanCodes/ethical-compass-backend
   cd ethical-compass-backend
   ```

2. **Set up a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Linux/Mac
   venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 📥 Model Setup

You must download the pretrained model weights before running the API.

1. Download the `model.safetensors` file from the provided link:  
   👉 [Download Model Weights](https://drive.google.com/file/d/1iKaDIIGBvYqg56EEhQr1Xlivlb1xaokv/view?usp=sharing)

2. Place it inside the following directory:  
   ```
   ml_models/ethics_prediction_deberta_v3_small/
   ```

   After setup, your structure should look like this:
   ```
   Ethical-Compass/
   ├── app/
   ├── ml_models/
   │   └── ethics_prediction_deberta_v3_small/
   │       └── model.safetensors
   ├── requirements.txt
   └── README.md
   ```

---

## ▶️ Running the API

From the project **root directory**, run:

```bash
python -m app.main
```

This will start the server at:

```
http://0.0.0.0:8000
```

---

## 📡 API Usage

### **POST** `/predict`

#### Request
```json
{
  "text": "Lying to a friend to avoid hurting their feelings"
}
```

#### Response
```json
{
  "ethics_score": -0.866,
  "label": "Unethical",
  "probability_ethical": 0.067
}
```

---

## 📂 Project Structure

```
Ethical-Compass/
├── app/
│   ├── main.py                # Flask entrypoint
│   ├── config.py              # Config settings
│   ├── routes/
│   │   └── predict.py         # /predict endpoint
│   └── services/
│       └── combined_inference.py  # EthicsPipeline
├── ml_models/
│   └── ethics_prediction_deberta_v3_small/
│       └── model.safetensors  # Downloaded model weights
├── requirements.txt
└── README.md
```

---

## 📜 License

MIT License. Free to use and modify.
