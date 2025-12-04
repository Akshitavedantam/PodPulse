from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# 1. Initialize App & Tools
app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

# CORS (Allow Frontend to talk to Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Define Input Schema
class SegmentRequest(BaseModel):
    text: str

# 3. Load Model
# We go up two levels because this file is in podpulse/backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_engine", "podpulse_model.pkl")

print(f"Loading model from: {MODEL_PATH}")

try:
    with open(MODEL_PATH, "rb") as f:
        model_pipeline = pickle.load(f)
    print("✅ Hybrid Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Model file not found. Please run train_model.py first.")
    model_pipeline = None

# 4. Feature Extraction Helper (Mirroring data_collector.py logic)
def extract_features(text):
    words = text.split()
    word_count = len(words) if len(words) > 0 else 1
    
    # 1. Sentiment
    sentiment = analyzer.polarity_scores(text)['compound']
    
    # 2. Questions
    questions = text.count("?")
    
    # 3. Fillers
    fillers = ["um", "uh", "like", "sort of", "you know", "basically", "literally", "mean"]
    filler_count = sum(1 for w in words if w.lower() in fillers)
    filler_ratio = filler_count / word_count
    
    # 4. Complexity (Avg Word Length)
    avg_len = sum(len(w) for w in words) / word_count
    
    # Return as DataFrame (because the Pipeline expects a DataFrame)
    return pd.DataFrame([{
        'text': text,
        'feature_sentiment': sentiment,
        'feature_questions': questions,
        'feature_fillers': filler_ratio,
        'feature_complexity': avg_len
    }])

# 5. Prediction Endpoint
@app.post("/predict")
def predict_engagement(request: SegmentRequest):
    if not model_pipeline:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Extract features
        features_df = extract_features(request.text)
        
        # ---------------------------------------------------------
        # 🧐 DEBUG PRINT: See exactly what the model sees
        # ---------------------------------------------------------
        print("\n" + "="*40)
        print("🔍 INPUT TEXT:", request.text[:50] + "...")
        print("-" * 40)
        print("📊 EXTRACTED FEATURES:")
        # Print the first row (series) to see values clearly
        print(features_df.iloc[0].to_string())
        print("-" * 40)
        
        # Predict
        prediction = model_pipeline.predict(features_df)[0]
        probs = model_pipeline.predict_proba(features_df)[0]
        
        print(f"🤖 PREDICTION: {prediction} (0=Good, 1=Bad)")
        print(f"📈 CONFIDENCE: {probs}")
        print("="*40 + "\n")
        # ---------------------------------------------------------

        confidence = round(max(probs) * 100, 2)

        return {
            "is_drop_off": int(prediction),
            "confidence_score": confidence,
            "message": "High Risk of Drop-off" if prediction == 1 else "High Engagement Segment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "PodPulse API is running 🚀"}