from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os

app = FastAPI()

class SegmentRequest(BaseModel):
    text: str
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_engine", "podpulse_model.pkl")

print(f"Loading model from: {MODEL_PATH}")

try:
    with open(MODEL_PATH, "rb") as f:
        model_pipeline = pickle.load(f)
    print(" Model loaded successfully!")
except FileNotFoundError:
    print("error: Model file not found.")
    model_pipeline = None

@app.post("/predict")
def predict_engagement(request: SegmentRequest):
    if not model_pipeline:
        raise HTTPException(status_code=500, detail="Model not loaded")

    prediction = model_pipeline.predict([request.text])[0]
    
    probs = model_pipeline.predict_proba([request.text])[0]
    confidence = round(max(probs) * 100, 2) 

    return {
        "is_drop_off": int(prediction),
        "confidence_score": confidence,
        "message": "High Risk of Drop-off" if prediction == 1 else "High Engagement Segment"
    }
@app.get("/")
def home():
    return {"status": "PodPulse API is running 🚀"}