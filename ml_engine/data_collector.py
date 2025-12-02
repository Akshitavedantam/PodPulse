import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import time
video_ids = [
    "L_Guz73e6fw", # Sam Altman 
    "DxREm3s1scA", # Mark Zuckerberg 
    "tN57WIUVDbk", # Sam Harris 
    "U0SKGq6M8P0", # MKBHD 
]
data = []

print("starting data collection ...")

yt = YouTubeTranscriptApi()

for video in video_ids :
    print(f"fetching the video data :{video}...")
    try:
        tx = yt.fetch(video)
        current_segment_text = ""
        segment_id = 0
        for item in tx:
            current_segment_text+=item.text+" "
            word_count = len(current_segment_text.split())
            if word_count>60:
                is_drop_off = 0
                if len(current_segment_text)>400:
                    is_drop_off = 1
                
                data.append({
                        "video_id":video ,
                        "segment_id":segment_id,
                        "text":current_segment_text.strip(),
                        "word_count":word_count,
                        "is_drop_off":is_drop_off,
                })
                current_segment_text=""
                segment_id+=1
        print(f"processed segment :{segment_id} for video {video}")
    except Exception as e:
        print(f"error occured while fetching video:{video},error:{str(e)}")
        
if len(data)>0:
    df =pd.DataFrame(data)
    df.to_csv("podcast_segments.csv",index=False)
    print(f" Data saved to: ml_engine/podcast_segments.csv")
else:
    print("\n Failed to collect data. Check your internet connection.")