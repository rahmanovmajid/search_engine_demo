import json
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def load_index():
    with open("data/pages_indexed.json", "r", encoding="utf-8") as f:
        pages = json.load(f)
    with open("data/tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    with open("data/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return pages, tfidf_matrix, vectorizer

def search(query, top_k=5):
    pages, tfidf_matrix, vectorizer = load_index()
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked_indices = similarities.argsort()[::-1][:top_k]
    
    results = []
    for idx in ranked_indices:
        result = {
            "title": pages[idx]["title"],
            "url": pages[idx]["url"],
            "score": float(similarities[idx]),
            "snippet": pages[idx]["content"][:300] + "..."
        }
        results.append(result)
    
    return results

if __name__ == "__main__":
    while True:
        query = input("\n🔍 Enter your search query (or type 'exit'): ")
        if query.lower() == 'exit':
            break
        results = search(query)
        for i, res in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Title: {res['title']}")
            print(f"URL: {res['url']}")
            print(f"Score: {res['score']:.4f}")
            print(f"Snippet: {res['snippet']}")
