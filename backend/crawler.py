
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import time
# import json
# import os

# SEED_URLS = [
#     "https://en.wikipedia.org/wiki/Web_search_engine",
#     "https://realpython.com/",
#     "https://developer.mozilla.org/en-US/docs/Web",
# ]

# CRAWL_LIMIT = 100
# TIMEOUT = 10
# HEADERS = {'User-Agent': 'MiniSearchBot/1.0'}

# visited = set()
# queue = SEED_URLS.copy()
# results = []

# def is_valid(url):
#     parsed = urlparse(url)
#     return parsed.scheme in ["http", "https"]

# def fetch_page(url):
#     try:
#         response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         title = soup.title.string.strip() if soup.title else "No Title"
#         paragraphs = soup.find_all('p')
#         content = ' '.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

#         return {
#             "url": url,
#             "title": title,
#             "content": content
#         }, soup
#     except Exception as e:
#         print(f"[Error] {url}: {e}")
#         return None, None

# def crawl():
#     while queue and len(results) < CRAWL_LIMIT:
#         url = queue.pop(0)
#         if url in visited:
#             continue
#         visited.add(url)

#         print(f"[{len(results)+1}/{CRAWL_LIMIT}] Crawling: {url}")
#         page_data, soup = fetch_page(url)
#         if not page_data:
#             continue

#         results.append(page_data)

#         # Extract links
#         if soup:
#             for link_tag in soup.find_all('a', href=True):
#                 href = link_tag['href']
#                 full_url = urljoin(url, href)
#                 if is_valid(full_url) and full_url not in visited and len(queue) + len(results) < CRAWL_LIMIT * 2:
#                     queue.append(full_url)

#         time.sleep(0.5)  # polite crawling

#     return results

# def save(results, path="data/pages.json"):
#     os.makedirs("data", exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(results, f, ensure_ascii=False, indent=2)

# if __name__ == "__main__":
#     results = crawl()
#     save(results)
#     print(f"✅ Crawled and saved {len(results)} pages.")
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import os
import random

# === SETTINGS ===
CRAWL_LIMIT = 1000
TIMEOUT = 10
SAVE_EVERY = 100
HEADERS = {'User-Agent': 'MiniSearchBot/1.0'}
SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)

# === SEED URLS (200 common and tech-related pages) ===
base_urls = [
    "https://en.wikipedia.org/wiki/",
    "https://www.geeksforgeeks.org/",
    "https://realpython.com/",
    "https://developer.mozilla.org/en-US/docs/Web",
    "https://www.bbc.com/news",
    "https://www.coursera.org/",
    "https://towardsdatascience.com/",
    "https://www.nytimes.com/",
    "https://www.python.org/",
    "https://docs.python.org/3/",
]

topics = [  # Generate many topic variations
    "Python_(programming_language)", "Web_search_engine", "Data_science", "Machine_learning",
    "Cybersecurity", "Algorithms", "Software_engineering", "Artificial_intelligence",
    "Natural_language_processing", "Operating_system", "Cloud_computing", "GitHub", "Docker",
    "Kubernetes", "HTML", "CSS", "JavaScript", "React", "Node.js", "Flask", "Django",
    "Linux", "Ubuntu", "Computer_vision", "Cryptography", "Robotics", "Deep_learning",
]

# Generate seed list from base_urls + random topics
SEED_URLS = list({url + topic for url in base_urls for topic in random.sample(topics, k=5)})
SEED_URLS = SEED_URLS[:200]  # Limit to 200 seeds

# === STATE ===
visited = set()
queue = SEED_URLS.copy()
results = []

# === HELPERS ===
def is_valid(url):
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"]

def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

        return {
            "url": url,
            "title": title,
            "content": content
        }, soup
    except Exception as e:
        print(f"[Error] {url}: {e}")
        return None, None

def save(results, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# === MAIN CRAWLER ===
def crawl():
    while queue and len(results) < CRAWL_LIMIT:
        url = queue.pop(0)
        norm_url = normalize_url(url)
        if norm_url in visited:
            continue
        visited.add(norm_url)

        print(f"[{len(results)+1}/{CRAWL_LIMIT}] Crawling: {url}")
        page_data, soup = fetch_page(url)
        if not page_data or len(page_data["content"]) < 200:
            continue  # Skip short content

        results.append(page_data)

        # Save progress
        if len(results) % SAVE_EVERY == 0:
            save(results, f"{SAVE_DIR}/pages_checkpoint_{len(results)}.json")
            print(f"💾 Saved checkpoint at {len(results)} pages.")

        # Extract and queue new links
        if soup:
            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                full_url = urljoin(url, href)
                norm_full = normalize_url(full_url)
                if is_valid(full_url) and norm_full not in visited and len(queue) + len(results) < CRAWL_LIMIT * 2:
                    queue.append(full_url)

        time.sleep(1)  # Polite crawling

    return results

# === EXECUTE ===
if __name__ == "__main__":
    final_results = crawl()
    save(final_results, f"{SAVE_DIR}/pages_final.json")
    print(f"\n✅ Done! Crawled and saved {len(final_results)} pages.")
