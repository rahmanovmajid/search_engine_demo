import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def load_pages(path="data/pages.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_index(pages):
    documents = [page['content'] for page in pages]
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9)
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer

def save_index(tfidf_matrix, vectorizer, pages):
    os.makedirs("data", exist_ok=True)
    with open("data/tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)
    with open("data/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("data/pages_indexed.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pages = load_pages()
    tfidf_matrix, vectorizer = build_index(pages)
    save_index(tfidf_matrix, vectorizer, pages)
    print("✅ TF-IDF index built and saved.")
