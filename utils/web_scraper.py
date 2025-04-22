
# utils/web_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_reddit(keyword, max_posts=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.reddit.com/search/?q={keyword}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    posts = []
    for post in soup.select('a[data-click-id="body"]')[:max_posts]:
        posts.append({"platform": "Reddit", "comment": post.get_text(strip=True)})
    
    return pd.DataFrame(posts)

def scrape_trustpilot(keyword, max_reviews=10):
    return pd.DataFrame([
        {"platform": "Trustpilot", "comment": f"Sample Trustpilot review for {keyword} #{i+1}"}
        for i in range(max_reviews)
    ])
