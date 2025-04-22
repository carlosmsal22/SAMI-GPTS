
# utils/web_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_reddit(keyword: str, max_posts: int = 20):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.reddit.com/search/?q={keyword}&sort=new"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for post in soup.select('a[data-click-id="body"]')[:max_posts]:
        text = post.get_text(strip=True)
        if text:
            results.append({"platform": "Reddit", "comment": text})

    return pd.DataFrame(results)


def scrape_trustpilot(keyword: str, max_reviews: int = 20):
    base_url = f"https://www.trustpilot.com/search?query={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for review in soup.find_all("p", class_=re.compile(".*review-content__text.*"))[:max_reviews]:
        text = review.get_text(strip=True)
        if text:
            results.append({"platform": "Trustpilot", "comment": text})

    return pd.DataFrame(results)


def scrape_google_reviews(keyword: str, max_reviews: int = 20):
    # Placeholder: Google reviews typically require APIs or headless browser automation.
    # Returning dummy placeholder.
    return pd.DataFrame([{"platform": "Google", "comment": f"Sample Google review for {keyword}."} for _ in range(max_reviews)])
