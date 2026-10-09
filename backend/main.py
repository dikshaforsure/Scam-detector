"""FastAPI service for SMS and message scam triage.

This is a defensive screening aid, not proof that a message is safe. The
classic TF-IDF model is combined with transparent lexical risk indicators;
the indicators are explanations, not an independently calibrated probability.
"""
from pathlib import Path
import os
import pickle
import re
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent


def load_artifact(filename: str) -> Any:
    path = BASE_DIR / filename
    if not path.exists():
        raise RuntimeError(
            f"Required artifact missing: {path}. Run the training script "
            "or restore the committed model artifacts."
        )
    with path.open("rb") as artifact:
        return pickle.load(artifact)


model = load_artifact("model.pkl")
vectorizer = load_artifact("vectorizer.pkl")

app = FastAPI(
    title="Scam Detector API",
    description="NLP-based message screening with transparent risk indicators.",
    version="2.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


class MessageInput(BaseModel):
    message: str = Field(min_length=1, max_length=10000)

    @field_validator("message")
    @classmethod
    def message_must_contain_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message must contain non-whitespace text.")
        return value.strip()


URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>]+")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)")
CURRENCY_RE = re.compile(r"(?i)(?:₹|\b(?:inr|rs\.?|usd|\$)\s?\d)")
RISK_PATTERNS = {
    "Urgency or account threat": re.compile(
        r"\b(?:urgent|immediately|within\s+\d+\s+(?:hours?|minutes?)|"
        r"account (?:blocked|suspended)|will be blocked|deactivated|expire today)\b",
        re.I,
    ),
    "Credential or secret request": re.compile(
        r"\b(?:share|send|confirm|provide|verify|enter)\b.{0,55}"
        r"\b(?:otp|one[- ]time password|password|pin|upi pin|cvv|bank details|aadhaar)\b"
        r"|\b(?:otp|upi pin|password|cvv)\b.{0,35}\b(?:share|send|confirm|provide|enter)\b",
        re.I,
    ),
    "Reward or prize bait": re.compile(
        r"\b(?:you (?:have )?won|winner|lottery|prize|claim (?:your )?(?:reward|cash|refund)|"
        r"free gift|cashback|guaranteed returns)\b",
        re.I,
    ),
    "Payment pressure": re.compile(
        r"\b(?:pay now|transfer (?:the )?money|send money|release payment|"
        r"processing fee|security deposit|pay to receive)\b",
        re.I,
    ),
    "Remote-access or impersonation language": re.compile(
        r"\b(?:customer care|support team|police|customs|tax department|rbi|"
        r"bank officer|remote access|install (?:this )?app)\b",
        re.I,
    ),
}


def explain_risk(message: str) -> list[dict[str, str]]:
    indicators: list[dict[str, str]] = []
    urls = URL_RE.findall(message)
    if urls:
        indicators.append({
            "title": "Contains a link",
            "detail": f"{len(urls)} URL-like item(s); inspect the real domain before opening.",
            "severity": "medium",
        })
    for title, pattern in RISK_PATTERNS.items():
        if pattern.search(message):
            indicators.append({
                "title": title,
                "detail": "A phrase associated with common social-engineering attempts was found.",
                "severity": "high" if title in {
                    "Credential or secret request", "Payment pressure"
                } else "medium",
            })
    if CURRENCY_RE.search(message):
        indicators.append({
            "title": "Money amount mentioned",
            "detail": "Money language can be normal; check whether it is paired with pressure or a request for sensitive information.",
            "severity": "low",
        })
    if PHONE_RE.search(message):
        indicators.append({
            "title": "Phone-number-like pattern",
            "detail": "Verify any phone number through an independently trusted source.",
            "severity": "low",
        })
    return indicators


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Scam Detector API is running", "docs": "/docs", "version": "2.0.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": type(model).__name__, "vectorizer": type(vectorizer).__name__}


@app.post("/predict")
def predict(data: MessageInput) -> dict[str, Any]:
    message = data.message
    try:
        transformed = vectorizer.transform([message])
        prediction = int(model.predict(transformed)[0])
    except Exception as exc:  # surface a clear API error without leaking message text
        raise HTTPException(status_code=500, detail="Model inference failed. Check model artifacts and dependency versions.") from exc

    risk_indicators = explain_risk(message)
    label = "scam" if prediction == 1 else "likely_safe"
    # SVM margins are not calibrated probabilities; deliberately do not present
    # them as confidence percentages.
    return {
        "input_message": message,
        "label": label,
        "prediction": "Scam message" if prediction == 1 else "No scam pattern detected",
        "risk_indicators": risk_indicators,
        "indicator_count": len(risk_indicators),
        "disclaimer": (
            "Automated screening can be wrong. A 'likely safe' result is not a guarantee; "
            "never share OTPs, PINs, passwords, or payment credentials."
        ),
    }
