import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

def scrape_reddit(keyword, max_posts=10):
    """Working Reddit scraper using official API"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        url = f"https://www.reddit.com/search.json?q={keyword}&limit={max_posts}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()['data']['children']
        posts = [{
            'comment': post['data']['title'],
            'source': 'Reddit',
            'date': datetime.fromtimestamp(post['data']['created_utc']),
            'url': f"https://reddit.com{post['data']['permalink']}"
        } for post in data]
        
        return pd.DataFrame(posts)
    except Exception as e:
        print(f"Reddit error: {e}")
        return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Working Trustpilot scraper with modern selectors"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        # First find business page
        search_url = f"https://www.trustpilot.com/search?query={keyword}"
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract business link
        business_link = soup.find('a', {'class': 'link_internal__7XN06'})
        if not business_link:
            return pd.DataFrame()
            
        # Scrape reviews from business page
        reviews_url = f"https://www.trustpilot.com{business_link['href']}"
        response = requests.get(reviews_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('.styles_reviewCard__hcAvl')[:max_reviews]:
            try:
                reviews.append({
                    'comment': review.select_one('.styles_reviewContent__0Q2Tg').get_text(strip=True),
                    'source': 'Trustpilot',
                    'date': review.select_one('time').get('datetime'),
                    'rating': len(review.select('.star-rating_starRating__4FncY img[alt*="star"]'))
                })
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Skipping review: {e}")
                continue
                
        return pd.DataFrame(reviews)
    except Exception as e:
        print(f"Trustpilot error: {e}")
        return pd.DataFrame()
