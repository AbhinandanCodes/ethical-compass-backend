# Ethical Compass 🧭

A lightweight ethics evaluation API that predicts whether a given scenario is **Ethical** or **Unethical**, along with a continuous ethics score and probability.  
You provide a **situation** and an **action**, and the API returns ethical classification results (from Layer 1) and emotional tone analysis (from Layer 2) — giving a complete ethical context for the scenario.

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
   venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 📥 Model Setup

You must download the pretrained model weights before running the API.

### 🔹 Layer 1 – Ethics Classification Model
1. Download the `model.safetensors` file for **Layer 1 (Ethics Model)** from the following link:  
   👉 [Download Layer 1 Model Weights](https://drive.google.com/file/d/1iEn5sNRxmZiwry8MqkFc0IrnRivyuOAR/view?usp=sharing)

2. Place it inside the following directory:  
   ```
   layers/layer1/model/
   ```

   **After setup, your structure should look like:**
   ```
   Ethical-Compass/
   ├── layers/
   │   ├── layer1/
   │   │   └── model/
   │   │       └── model.safetensors
   ```

---

### 🔹 Layer 2 – Emotion Classification Model
1. Download the `model.safetensors` file for **Layer 2 (Emotion Model)** from the following link:  
   👉 [Download Layer 2 Model Weights](https://drive.google.com/file/d/1aWXUfi5T4Ub5vmIdJU0TcSzQTb-YWPid/view?usp=sharing)

2. Place it inside the following directory:  
   ```
   layers/layer2/model/
   ```

   **After setup, your structure should look like:**
   ```
   Ethical-Compass/
   ├── layers/
   │   ├── layer2/
   │   │   └── model/
   │   │       └── model.safetensors
   ```

---

## ▶️ Running the API

From the project **root directory**, run:

```bash
python -m src.main
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
  "situation": "You find a lost wallet on the street",
  "action": "You return it to the owner"
}
```

#### Response
```json
{
  "layer1": "Label: Ethical, Ethical: 97.9% Unethical: 2.1%",
  "layer2": "93.13% neutral 1.81% realization 1.75% annoyance ",
  "text": "Situation: You find a lost wallet on the street. Action: You return it to the owner."
}
```

#### Example using curl
```bash
curl -X POST http://localhost:8000/predict ^ -H "Content-Type: application/json" ^ -d @req_data.json
```

---

## 📂 Project Structure

```
Ethical-Compass/
├── src/
│   ├── main.py                # Flask entrypoint
│   ├── config.py              # Config settings
│   ├── routes/
│   │   └── predict.py         # /predict endpoint
│   └── services/
│       └── ethical_compass.py  # EthicalCompass

├── layers/
│   ├── layer1/
│   │   └── model/
│   │       └── model.safetensors
│   └── layer2/
│       └── model/
│           └── model.safetensors

├── requirements.txt
└── README.md
```

---

## 📜 License

MIT License. Free to use and modify.
