<div align="center">

<h1 align="center">🎙️ PodPulse</h1>

<p align="center"><strong><b>AI-Powered Content Intelligence Engine<b/></strong></p>

<p align="center">
Predict listener drop-off points before you record.<br>
Trained on 2,000+ viral segments from Lex Fridman, MrBeast, and TED Talks.
</p>
</div>

# ❗The Problem 

Content creators rely on lagging indicators (views, retention graphs) to judge success. By the time they see the data, the episode is already published.

PodPulse solves this by providing leading indicators. It uses Natural Language Processing (NLP) to simulate listener psychology and flag "high-risk" script sections before production.

# check it out!

<p align="center">
  <a href="https://podpulse-two.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-000000?style=flat&logo=vercel&logoColor=white" alt="Live Demo"/>
  </a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Akshitavedantam/PodPulse/main/assets/demo.png" alt="Dashboard Preview" width="100%">
</p>

# 📐Architecture

| Component | Tech Stack | Responsibility |
| :--- | :--- | :--- |
|  Brain | `scikit-learn` | Hybrid Random Forest Classifier (Text + Metadata). |
|  API | `FastAPI` | Real-time inference engine (<100ms latency). |
|  UI | `Next.js 14` | Interactive engagement dashboard. |
|  Data | `YouTube API` | Custom scraper for building the 2k+ sample dataset. |

# 🚀 Quick Start

1. Clone & Setup
   
  ```bash
git clone [https://github.com/Akshitavedantam/PodPulse.git](https://github.com/Akshitavedantam/PodPulse.git)
cd PodPulse
```


2. Launch Backend (API)
```bash
cd backend
python -m venv venv
```
# Activate Environment
# Windows:
```bash
.\venv\Scripts\Activate.ps1
```
# Mac/Linux:
```bash
source venv/bin/activate
```
# Install & Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Launch Frontend (UI)
```bash
cd frontend
npm install
npm run dev
```


👉 Open http://localhost:3000 to test the engagement engine.

🧠 Model Logic

 The model analyzes 4 proxies for human boredom:

* <u>Sentiment Volatility:</u> (VADER) High emotion correlates with retention.

* <u>Interaction Hooks:</u>  Question marks (?) re-engage listener attention.

* <u>Cognitive Load:</u>  High average word length without breaks fatigues the listener.

* <u>Speech Quality:</u>  High filler word ratio (um, like) signals low confidence.

📊 Performance

Accuracy: ~89% (Validation Set)

Dataset: 50/50 Balanced Split (High vs Low Engagement)

📜 License

Distributed under the MIT License.
<p align="right">
  <i>Designed & Developed by</i><br>
  <b>Akshita Vedantam</b>
</p>
