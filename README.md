PodPulse

PodPulse is a content intelligence engine that analyzes podcast transcripts to predict listener retention. By combining linguistic complexity metrics with sentiment volatility analysis, it identifies high-risk drop-off points in audio content before production.

The system was trained on a custom dataset of 5,000+ segments aggregated from high-performing (e.g., Lex Fridman, MrBeast) vs. low-performing audio transcripts, achieving an F1-score of ~0.89 on the validation set.

📸 Dashboard Preview

Core Features

Predictive Scoring: Binary classification model (Random Forest) to flag "At-Risk" vs. "Optimized" segments.

Multimodal Feature Extraction:

Sentiment Volatility: Measures emotional variance using VADER (monotone vs. dynamic).

Cognitive Load: Calculates lexical density and sentence complexity.

Hook Detection: Identifies interrogative structures that drive re-engagement.

Real-time Inference: sub-100ms API response time using FastAPI.

System Architecture

The project follows a decoupled Client-Server architecture:

ML Pipeline (/ml_engine)

Data Ingestion: Custom scraper (youtube-transcript-api) handling rate limits and parsing.

Preprocessing: scikit-learn pipeline with ColumnTransformer for text (TF-IDF) and numeric scaling.

Model: Hybrid Random Forest Classifier (100 estimators).

Backend API (/backend)

FastAPI: Exposes a /predict REST endpoint.

On-the-fly Engineering: Raw text inputs are processed through the same feature extraction pipeline used during training to ensure consistency.

Frontend (/frontend)

Next.js 14: Server-side rendering and static optimization.

Visualization: Interactive engagement charts using recharts.

Local Development

Prerequisites

Python 3.10+

Node.js 18+

1. Backend Setup

# Clone repository
git clone [https://github.com/YOUR_USERNAME/PodPulse.git](https://github.com/YOUR_USERNAME/PodPulse.git)
cd PodPulse

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Install dependencies & run server
pip install -r requirements.txt
cd backend
uvicorn main:app --reload


2. Frontend Setup

cd frontend
npm install
npm run dev


The application will be available at http://localhost:3000.

License

This project is licensed under the MIT License - see the LICENSE file for details.