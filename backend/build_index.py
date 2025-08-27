from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle
import os

# Load content
with open("data/pages_final.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

corpus = [page["content"] for page in pages]

# Train vectorizer
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    max_df=0.9,
    min_df=2
)
tfidf_matrix = vectorizer.fit_transform(corpus)

# Save vectorizer and matrix
os.makedirs("data", exist_ok=True)

with open("data/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("data/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

with open("data/pages_indexed.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

print("✅ Index built and saved.")
