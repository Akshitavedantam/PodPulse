import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
try:
    df = pd.read_csv("podcast_segments.csv")
    print(f"  Loaded {len(df)} segments of data")
except FileNotFoundError:
    print(" Error: podcast_segments.csv not found.make sure data exists.")
    exit()

X = df['text'].fillna("")
y = df['is_drop_off']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
print("   ... Training the Random Forest model")
pipeline.fit(X_train, y_train)
print("Model Performance Report:")
predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions))

with open("podpulse_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print(" Model saved as 'podpulse_model.pkl'.")
