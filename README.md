
# Ethical Compass 🧭

A lightweight ethics evaluation API that predicts whether a given scenario is:

- **Ethical vs Unethical** (Layer 1)
- **Emotional tone & reaction spectrum** (Layer 2)
- **Moral Policing Vulnerability Score** – likelihood of externally imposed moral judgment (Layer 3)

You provide a **situation** and an **action**, and the API returns a multi-layer ethical profile.

---

## 🚀 Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/AbhinandanCodes/ethical-compass-backend
cd ethical-compass-backend
```

2️⃣ **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 📥 Model Setup

### 🔹 Layer 1 – Ethics Classification Model
Download the **Layer 1 Weights**:  
👉 [Download Model Weights](https://drive.google.com/file/d/1iEn5sNRxmZiwry8MqkFc0IrnRivyuOAR/view?usp=drive_link)

Place here:

```
layers/layer1/model/
```

---

### 🔹 Layer 2 – Emotion Classification Model
Download the **Layer 2 Weights**:  
👉 [Download Model Weights](https://drive.google.com/file/d/1aWXUfi5T4Ub5vmIdJU0TcSzQTb-YWPid/view?usp=drive_link)

Place here:

```
layers/layer2/model/
```

---

### 🔹 Layer 3 – Moral Policing Vulnerability Model
Download the **Layer 3 Weights**:  
👉 [Download Model Weights](https://drive.google.com/file/d/1yQp4HrcBSho1DuHduyew0kRF4uyqmNfw/view?usp=sharing)

Place here:

```
layers/layer3/model/
```

---

### 📚 Final Model Folder Structure

```
Ethical-Compass/
├── layers/
│   ├── layer1/
│   │   └── model/
│   │       └── model.safetensors
│   ├── layer2/
│   │   └── model/
│   │       └── model.safetensors
│   └── layer3/
│       └── model/
│           └── model.safetensors
```

---

## ▶️ Running the API
From the project **root** folder:

```bash
python -m src.main
```

Server starts at:

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

---

### 📥 Updated Sample Response

```json
{
  "input_text": "Situation: You find a lost wallet on the street. Action: You return it to the owner.",
  "layer1_ethics": {
    "label": "Ethical",
    "scores": {
      "ethical": 97.9,
      "unethical": 2.1
    }
  },
  "layer2_emotions": [
    {
      "emotion": "neutral",
      "score": 92.75
    },
    {
      "emotion": "realization",
      "score": 2.05
    },
    {
      "emotion": "annoyance",
      "score": 1.96
    }
  ],
  "layer3_policing": {
    "policing_index": 31.6
  }
}
```

---

## 🧱 Project Structure

```
Ethical-Compass/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   └── predict.py
│   └── services/
│       └── ethical_compass.py
├── layers/
│   ├── layer1/
│   ├── layer2/
│   └── layer3/
├── requirements.txt
└── README.md
```

---

## 📜 License
MIT License — free to use and modify.
