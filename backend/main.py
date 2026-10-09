from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Input format
class MessageInput(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Scam Detection API Running"}

@app.post("/predict")
def predict(data: MessageInput):

    message = data.message

    # Convert text to TF-IDF features
    transformed = vectorizer.transform([message])

    # Predict
    prediction = model.predict(transformed)[0]
    print("Prediction:", prediction)
    result = "🚨 Scam Message" if prediction == 1 else "✅ Safe Message"

    return {
        "input_message": message,
        "prediction": result
    }