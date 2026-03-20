# 🛡️ Network Security — Phishing URL Detection System

> An end-to-end ML pipeline that detects phishing URLs using automated model selection, MLflow experiment tracking, a custom 30-feature extractor, and a Flask web interface.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-websitechecker--askr.onrender.com-00d4aa?style=for-the-badge)](https://websitechecker-askr.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![MLflow](https://img.shields.io/badge/MLflow-Tracked-0194E2?style=for-the-badge)](https://mlflow.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb)](https://mongodb.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge)](https://render.com)

---

## 🚀 Live Demo

**[websitechecker-askr.onrender.com](https://websitechecker-askr.onrender.com/)**

> ⚠️ Hosted on Render free tier — first request may take ~30s to wake the service.

---

## What It Does

Paste any URL → the system extracts 30 engineered features → runs a strict phishing rule layer → passes through a trained ML model → returns **SAFE** or **UNSAFE** in real time.

The training pipeline automatically selects the best-performing model from 5 candidates. Every experiment is tracked with MLflow so results are fully reproducible. Training data is ingested directly from MongoDB Atlas.

---

## ML Pipeline

### End-to-End Training Flow
```
MongoDB Atlas (phishing dataset)
        │
        ▼
Data Ingestion      ← pymongo, train/test split
        │
        ▼
Data Validation     ← schema.yaml checks
        │
        ▼
Data Transformation ← preprocessor fitted + saved as .pkl
        │
        ▼
Model Trainer       ← 5 models evaluated, best selected by F1
        │
        ▼
MLflow Tracking     ← f1, precision, recall logged per run
        │
        ▼
final_model/model.pkl + preprocessor.pkl
```

### Automated Model Selection
5 models trained and evaluated — best performer selected automatically:

| Model | Evaluated |
|-------|-----------|
| Random Forest | ✅ |
| Decision Tree | ✅ |
| Gradient Boosting | ✅ |
| Logistic Regression | ✅ |
| AdaBoost | ✅ |

### Metrics (MLflow Tracked)
| Metric | Score |
|--------|-------|
| F1 Score | `[update after mlflow ui check]` |
| Precision | `[update after mlflow ui check]` |
| Recall | `[update after mlflow ui check]` |

> Run `mlflow ui` locally to view full experiment history.

---

## Custom Feature Extractor — 30 URL Features

Built from scratch in `feature_extracter.py`. Features include:

**Domain Analysis**
- Domain entropy (Shannon entropy of domain string)
- Domain length and token count
- Subdomain depth
- IP address in URL detection

**Strict Phishing Signals (Rule-based scoring layer)**
- Brand impersonation detection (PayPal, Google, Amazon, Microsoft, SBI, HDFC, Axis)
- URL shortener detection (bit.ly, goo.gl, tinyurl, t.co etc.)
- Suspicious TLD detection (.xyz, .top, .buzz, .tk, .zip, .cam etc.)
- Suspicious keyword detection (secure, verify, login, bank, payment, invoice etc.)

**URL Structure**
- Special character ratios
- HTTPS presence
- URL length
- Query string analysis

---

## What It Detects

- ✅ Fake login pages
- ✅ Brand impersonation (PayPal, Google, banks)
- ✅ Shortened phishing links (bit.ly etc.)
- ✅ IP-based phishing servers
- ✅ High-entropy (randomised) domains
- ✅ Suspicious TLDs
- ✅ Delivery and banking scam URLs

---

## Tech Stack

```
ML Pipeline   →  scikit-learn (5 models), NetworkModel (preprocessor + model wrapper)
Experiment    →  MLflow (f1, precision, recall tracked per run)
Data          →  MongoDB Atlas (training data), 100K synthetic + real phishing dataset
Backend       →  Flask (single-page app — session-based, no async required)
Deployment    →  Render (render.yaml config)
```

> Flask was chosen intentionally over FastAPI — this is a single-page synchronous app with no streaming or concurrent I/O. Flask is the simpler, more appropriate tool here.

---

## Project Structure

```
NetworkSecurity/
├── app.py                              # Flask app — session-based result (no refresh duplicate)
├── main.py                             # Training pipeline entry point
├── push_data.py                        # MongoDB data upload script
├── data_schema/schema.yaml             # Feature schema for validation
├── final_model/
│   ├── model.pkl                       # Best trained model
│   └── preprocessor.pkl               # Fitted preprocessor
├── Network_Data/
│   ├── phisingData.csv                 # Real phishing dataset
│   ├── synthetic_phishing_features_100k.csv
│   └── synthetic_phishing_features_10k.csv
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py           # MongoDB → DataFrame
│   │   ├── data_validation.py          # Schema checks
│   │   ├── data_transformation.py      # Preprocessing pipeline
│   │   └── model_trainer.py            # Multi-model eval + MLflow
│   ├── pipeline/
│   │   ├── training_pipeline.py        # Full pipeline orchestration
│   │   └── batch_prediction.py
│   ├── utils/
│   │   ├── main_utils/
│   │   │   ├── feature_extracter.py    # 30-feature URL extractor
│   │   │   └── utils.py
│   │   └── ml_utils/
│   │       ├── model/estimator.py      # NetworkModel class
│   │       └── metric/classification_metric.py
│   ├── entity/
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── exception/exception.py
│   └── logging/logger.py
├── templates/index.html                # Cyber-themed frontend
├── render.yaml                         # Render deployment config
└── requirements.txt
```

---

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/Akhilesh0605/NetWorkSecurity.git
cd NetWorkSecurity
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
# Create .env file
MONGO_DB_URL=your_mongodb_connection_string
SESSION_KEY=your_flask_secret_key
```

### 3. Run the web app

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

### 4. Re-run training pipeline (optional)

```bash
python main.py
```

This re-runs full pipeline: MongoDB ingestion → validation → transformation → model selection → MLflow tracking.

### 5. View MLflow experiments

```bash
mlflow ui
```

Open: `http://localhost:5000`

---

## Test URLs

**Should return UNSAFE:**
```
https://security-paypal-com.us/login
http://bit.ly/secure-update-login
https://google.com.security-alert.xyz
http://192.168.0.77/login.php
https://dhl.track-delivery-alert.shop
```

**Should return SAFE:**
```
https://www.google.com
https://www.github.com
https://www.microsoft.com
https://www.amazon.com
https://www.sbi.co.in
```

---

## Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Web Application | Render | [websitechecker-askr.onrender.com](https://websitechecker-askr.onrender.com/) |

Deployment configured via `render.yaml` in repo root.

---

## Built By

**Akhilesh Kovelakuntla** — 3rd Year CS Student  
Building end-to-end ML systems for real-world security problems.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Akhilesh%20Kovelakuntla-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/akhilesh-kovelakuntla-09a488265)
[![GitHub](https://img.shields.io/badge/GitHub-Akhilesh0605-181717?style=flat&logo=github)](https://github.com/Akhilesh0605)

---

## Disclaimer

This project is for educational and cybersecurity research purposes only.  
Do not open phishing URLs directly in your browser.