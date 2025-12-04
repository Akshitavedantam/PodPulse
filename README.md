<div align="center">

🎙️ PodPulse

AI-Powered Content Intelligence Engine

<br />

<p align="center">
<b>Predict listener drop-off points before you record.</b><br />
Trained on 5,000+ viral segments from Lex Fridman, MrBeast, and TED Talks.
</p>

</div>

 The Problem

Content creators rely on lagging indicators (views, retention graphs) to judge success. By the time they see the data, the episode is already published.

PodPulse solves this by providing leading indicators. It uses Natural Language Processing (NLP) to simulate listener psychology and flag "high-risk" script sections before production.

 Architecture

Component

Tech Stack

Responsibility

 Brain

scikit-learn

Hybrid Random Forest Classifier (Text + Metadata).

 API

FastAPI

Real-time inference engine (<100ms latency).

 UI

Next.js 14

Interactive engagement dashboard.

 Data

YouTube API

Custom scraper for building the 5k+ sample dataset.

 Quick Start

1. Clone & Setup

git clone [https://github.com/Akshitavedantam/PodPulse.git](https://github.com/Akshitavedantam/PodPulse.git)
cd PodPulse


2. Launch Backend (API)

cd backend
python -m venv venv

# Activate Environment
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install & Run
pip install -r requirements.txt
uvicorn main:app --reload


3. Launch Frontend (UI)

cd frontend
npm install
npm run dev


👉 Open http://localhost:3000 to test the engagement engine.

🧠 Model Logic

The model analyzes 4 proxies for human boredom:

Sentiment Volatility: (VADER) High emotion correlates with retention.

Interaction Hooks: Question marks (?) re-engage listener attention.

Cognitive Load: High average word length without breaks fatigues the listener.

Speech Quality: High filler word ratio (um, like) signals low confidence.

📊 Performance

Accuracy: ~89% (Validation Set)

Dataset: 50/50 Balanced Split (High vs Low Engagement)

📜 License

Distributed under the MIT License.