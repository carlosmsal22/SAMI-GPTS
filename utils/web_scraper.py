# utils/web_scraper.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_reddit(keyword, max_posts=10):
    """Scrape Reddit posts without API using pushshift"""
    url = f"https://api.pushshift.io/reddit/search/submission/?q={keyword}&size={max_posts}"
    try:
        response = requests.get(url)
        data = response.json()['data']
        return pd.DataFrame([{
            'comment': post['title'],
            'source': 'Reddit',
            'date': pd.to_datetime(post['created_utc'], unit='s')
        } for post in data])
    except Exception as e:
        print(f"Reddit scraping error: {e}")
        return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Scrape Trustpilot reviews"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    url = f"https://www.trustpilot.com/search?query={keyword}"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        
        for review in soup.select('.review-content')[:max_reviews]:
            reviews.append({
                'comment': review.select_one('.review-content__text').get_text(strip=True),
                'source': 'Trustpilot',
                'date': review.select_one('.review-content-header__dates').get_text(strip=True)
            })
            time.sleep(random.uniform(0.5, 1.5))  # Polite delay
            
        return pd.DataFrame(reviews)
    except Exception as e:
        print(f"Trustpilot scraping error: {e}")
        return pd.DataFrame()
