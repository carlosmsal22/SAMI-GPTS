import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

def scrape_reddit(keyword, max_posts=10):
    """Working Reddit scraper using Pushshift API"""
    print(f"Scraping Reddit for: {keyword}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Using Pushshift API
        url = f"https://api.pushshift.io/reddit/search/submission/?q={keyword}&size={max_posts}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()['data']
        posts = [{
            'comment': post['title'],
            'source': 'Reddit',
            'date': datetime.fromtimestamp(post['created_utc']),
            'url': f"https://reddit.com{post['permalink']}"
        } for post in data]
        
        print(f"Found {len(posts)} Reddit posts")
        return pd.DataFrame(posts)
        
    except Exception as e:
        print(f"Reddit scraping error: {e}")
        return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Working Trustpilot scraper with direct review page"""
    print(f"Scraping Trustpilot for: {keyword}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        # Directly access the review page for known brands
        brand_mapping = {
            'apple': 'apple.com',
            'nike': 'nike.com',
            'starbucks': 'starbucks.com'
        }
        
        domain = brand_mapping.get(keyword.lower())
        if not domain:
            return pd.DataFrame()
            
        url = f"https://www.trustpilot.com/review/{domain}"
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('article.review')[:max_reviews]:
            try:
                reviews.append({
                    'comment': review.select_one('.review-content__text').get_text(strip=True),
                    'source': 'Trustpilot',
                    'date': review.select_one('time')['datetime'],
                    'rating': len(review.select('.star-rating img[alt*="star"]'))
                })
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Skipping review: {e}")
                continue
                
        print(f"Found {len(reviews)} Trustpilot reviews")
        return pd.DataFrame(reviews)
        
    except Exception as e:
        print(f"Trustpilot scraping error: {e}")
        return pd.DataFrame()
