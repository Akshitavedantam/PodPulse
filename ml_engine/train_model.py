import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

print("Starting training pipeline...")

try:
    df = pd.read_csv("podcast_segments.csv")
    print(f"Loaded {len(df)} segments")
    
    required_cols = ['feature_sentiment', 'feature_questions', 'feature_fillers', 'feature_complexity']
    if not all(col in df.columns for col in required_cols):
        print("Missing required feature columns.")
        exit()
        
except FileNotFoundError:
    print("podcast_segments.csv not found.")
    exit()

text_col = 'text'
num_cols = ['feature_sentiment', 'feature_questions', 'feature_fillers', 'feature_complexity']

X = df[[text_col] + num_cols]
y = df['is_drop_off']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

text_pipe = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=3000))
])

num_pipe = Pipeline([
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer([
    ('text', text_pipe, text_col),
    ('num', num_pipe, num_cols)
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

model.fit(X_train, y_train)

print("\nEvaluation:")
preds = model.predict(X_test)
print(classification_report(y_test, preds))

with open("podpulse_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Saved model artifact: podpulse_model.pkl")