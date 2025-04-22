import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

# Sample data fallback
SAMPLE_DATA = {
    "Apple": [
        {"comment": "Love the new iPhone! Best camera ever", "source": "Reddit", "date": "2023-05-15"},
        {"comment": "Apple customer service needs improvement", "source": "Trustpilot", "date": "2023-04-20"},
        {"comment": "MacBook Pro is worth every penny", "source": "Reddit", "date": "2023-05-01"}
    ],
    "Nike": [
        {"comment": "Most comfortable running shoes I've owned", "source": "Reddit", "date": "2023-03-10"},
        {"comment": "Delivery was late but product quality is good", "source": "Trustpilot", "date": "2023-04-05"}
    ]
}

def scrape_reddit(keyword, max_posts=10):
    """Scraper with fallback to sample data"""
    print(f"Attempting to scrape Reddit for: {keyword}")
    try:
        # Try Pushshift API
        url = f"https://api.pushshift.io/reddit/search/submission/?q={keyword}&size={max_posts}"
        response = requests.get(url, timeout=10)
        data = response.json()['data']
        return pd.DataFrame([{
            'comment': post['title'],
            'source': 'Reddit',
            'date': datetime.fromtimestamp(post['created_utc'])
        } for post in data])
    except Exception as e:
        print(f"Using sample Reddit data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Reddit']
        return pd.DataFrame(sample[:max_posts])

def scrape_trustpilot(keyword, max_reviews=10):
    """Scraper with fallback to sample data"""
    print(f"Attempting to scrape Trustpilot for: {keyword}")
    try:
        # Try direct review page
        domain = {
            'apple': 'apple.com',
            'nike': 'nike.com'
        }.get(keyword.lower())
        if not domain:
            raise ValueError("Brand not in Trustpilot mapping")
            
        url = f"https://www.trustpilot.com/review/{domain}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('article.review')[:max_reviews]:
            reviews.append({
                'comment': review.select_one('.review-content__text').get_text(strip=True),
                'source': 'Trustpilot',
                'date': review.select_one('time')['datetime']
            })
        return pd.DataFrame(reviews)
    except Exception as e:
        print(f"Using sample Trustpilot data due to: {e}")
        sample = [d for d in SAMPLE_DATA.get(keyword, []) if d['source'] == 'Trustpilot']
        return pd.DataFrame(sample[:max_reviews])
