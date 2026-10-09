# Scam Detector

A defensive message-screening project that combines a TF-IDF text classifier with explainable social-engineering indicators. It is intended for learning and awareness, not as a guarantee that any message is safe.

## What's included

- React + Vite interface with responsive analysis and report panels.
- FastAPI inference API with input validation, health endpoint, configurable CORS, and clear result fields.
- Reproducible model training on CSV datasets with stratified hold-out evaluation.
- Evaluation report containing accuracy, scam precision/recall/F1, class counts, and confusion matrix.
- Rule-based indicators for links, credential requests, urgency, prizes, payment pressure, and impersonation language.

## Architecture

```text
React UI → FastAPI → TF-IDF vectorizer → Linear SVM
                         └─────────────→ interpretable risk indicators
```

The linear model and indicators provide two distinct signals. Indicator matches are not a probability, and model scores are not shown as calibrated confidence.

## Run locally

### 1. Backend

Python 3.10+ is recommended.

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API starts at `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`. Model artifacts are loaded relative to `main.py`, so launch location does not matter.

Optional: copy `backend/.env.example` settings to your deployment environment and set `CORS_ORIGINS` to a comma-separated list of exact trusted frontend origins.

### 2. Frontend

```bash
cd frontend-react
npm install
# Optional: copy .env.example to .env.local and set VITE_API_BASE_URL
npm run dev
```

The development interface is usually available at `http://localhost:5173`.

## Retrain and evaluate

CSV files in `dataset/` are used by default. The trainer expects text in a column named `Text`, `text`, `message`, `sms`, or `content`, and a binary target in `scam`, `label`, `target`, or `is_scam`. Values 0/ham/legitimate/safe map to legitimate; values 1/scam/spam/fraud/phishing map to scam.

```bash
cd backend
python train_model.py
```

Optional arguments:

```bash
python train_model.py --model logistic --test-size 0.2 --seed 42
python train_model.py --data ../dataset/sms_dataset_processed.csv
```

This writes `backend/evaluation.json` and replaces `model.pkl` and `vectorizer.pkl`. Keep the test split separate from model selection. Deduplication helps limit exact duplicates, but source leakage, synthetic examples, imbalanced classes, language shifts, and changing scam campaigns can inflate metrics. Review the class distribution and confusion matrix before using a model in a demo.

## API

`GET /` — service metadata

`GET /health` — basic health check

`POST /predict`

```json
{ "message": "Your bank account will be blocked. Share your OTP to continue." }
```

Returns `label` (`scam` or `likely_safe`), a human-readable `prediction`, `risk_indicators`, and a safety disclaimer. Messages must contain non-whitespace text and be at most 10,000 characters.

## Data and responsible use

Use datasets only when their licensing and provenance permit redistribution and research. Add samples from independent, documented sources; deduplicate before splitting; preserve the original label source; and evaluate across sources and time where possible. Avoid publishing personal data. This model is English-oriented unless training data proves otherwise.

A negative result is not assurance of safety. Do not send credentials or money based on a model result; confirm requests using a trusted channel. This project does not fetch or open suspicious URLs and does not monitor devices or messages in the background.
