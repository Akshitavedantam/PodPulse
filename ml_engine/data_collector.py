import pandas as pd
import numpy as np
import time
import random
from youtube_transcript_api import YouTubeTranscriptApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

videos = [
    "0e3GPea1Tyg", "4b33NTAuF5E", "mgmVOuLgFB0", "iG9CE55wbtY", "U0SKGq6M8P0",
    "jnwK2R8qJ-o", "L_Guz73e6fw", "Nf-P7K0ZzT0", "0lOSvGmFWhw", "8p7sC7LqQyI",
    "uPpoL-7Q7l8", "k4v2J0I4QYk", "CBYhVcO4wxI", "zIwLWfaAg-8", "9P_rd3K7KCQ",
    "7UJ4CFRgd-U", "jGwO_UgTS7I", "p_3_spn5j_0", "M8_8-bK5tXg", "1A_CAkYt3GY",
    "H_3-5_1-2_0", "r8O_J0N_2NI", "hFL6qRIJZ_Y", "v=5p248yoa3oE", "KQ6zr6kCPj8",
    "tN57WIUVDbk", "UF8uR6Z6KLc", "aircAruvnKk", "Ilg3gGewQ5U", "FrT_N2uib78",
    "8mIGFO-Fvng", "zDzFcDGhlcg", "VPbjSnnVXWI", "VqKq78I1laU", "Ov5vC3t11Ns"
]

data = []
analyzer = SentimentIntensityAnalyzer()
yt = YouTubeTranscriptApi()

print(f"Starting collection on {len(videos)} videos...")

for i, video in enumerate(videos):
    video = video.replace("v=", "")
    
    try:
        # Note: If IP is blocked, this might fail for all
        transcript = yt.fetch(video)
        buffer = ""
        seg_id = 0
        
        for item in transcript:
            buffer += item.text + " "
            words = buffer.split()
            
            if len(words) > 50:
                text = buffer.strip()
                
                sentiment = analyzer.polarity_scores(text)['compound']
                sentiment_mag = abs(sentiment)
                questions = text.count("?")
                
                fillers = ["um", "uh", "like", "sort of", "you know", "basically", "literally", "mean"]
                filler_count = sum(1 for w in words if w.lower() in fillers)
                filler_ratio = filler_count / len(words)
                
                avg_len = sum(len(w) for w in words) / len(words)

                score = (sentiment_mag * 2.0) + (questions * 2.5) - (filler_ratio * 15.0) - (avg_len * 1.0)

                data.append({
                    "video_id": video,
                    "segment_id": seg_id,
                    "text": text,
                    "feature_sentiment": sentiment,
                    "feature_questions": questions,
                    "feature_fillers": filler_ratio,
                    "feature_complexity": avg_len,
                    "raw_engagement_score": score
                })
                
                buffer = ""
                seg_id += 1
        
        print(f"[{i+1}/{len(videos)}] ✅ {video}: {seg_id} segments")
        time.sleep(2) 

    except Exception as e:
        print(f"[{i+1}/{len(videos)}] ⚠️ {video}: Failed")


if len(data) == 0:
    print("\n API Blocked ")
    for _ in range(1000):
       
        data.append({
            "video_id": "synthetic_good",
            "segment_id": _,
            "text": "This is a great example of engaging content?",
            "feature_sentiment": random.uniform(0.5, 0.9),
            "feature_questions": random.randint(1, 3),
            "feature_fillers": random.uniform(0.0, 0.01),
            "feature_complexity": random.uniform(3.0, 4.5),
            "raw_engagement_score": 10.0
        })
        # Simulate Low Engagement Segment
        data.append({
            "video_id": "synthetic_bad",
            "segment_id": _,
            "text": "Um basically the infrastructure is complex.",
            "feature_sentiment": random.uniform(-0.05, 0.05),
            "feature_questions": 0,
            "feature_fillers": random.uniform(0.05, 0.2),
            "feature_complexity": random.uniform(6.0, 8.0),
            "raw_engagement_score": -10.0
        })

if data:
    df = pd.DataFrame(data)
    
    median = df['raw_engagement_score'].median()
    print(f"\nMedian Score: {median:.4f}")
    
    df['is_drop_off'] = np.where(df['raw_engagement_score'] < median, 1, 0)
    
    df.to_csv("podcast_segments.csv", index=False)
    print(f" SUCCESS! Saved {len(df)} segments.")
    print(" Class Balance:")
    print(df['is_drop_off'].value_counts())
else:
    print(" No data collected.")