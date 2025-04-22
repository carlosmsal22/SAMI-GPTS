import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

def scrape_reddit(keyword, max_posts=10):
    """Scrape Reddit posts using alternative methods"""
    print(f"Attempting to scrape Reddit for: {keyword}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Method 1: Try official Reddit API
        url = f"https://www.reddit.com/search.json?q={keyword}&limit={max_posts}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()['data']['children']
        if data:
            print(f"Found {len(data)} posts via Reddit API")
            return pd.DataFrame([{
                'comment': post['data']['title'],
                'source': 'Reddit',
                'date': datetime.fromtimestamp(post['data']['created_utc'])
            } for post in data])
        
        # Fallback to HTML scraping if API fails
        print("Trying HTML fallback...")
        html_url = f"https://www.reddit.com/search/?q={keyword}"
        response = requests.get(html_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        posts = []
        for post in soup.select('h3')[:max_posts]:  # Common post title selector
            posts.append({
                'comment': post.get_text(strip=True),
                'source': 'Reddit',
                'date': datetime.now()
            })
        
        print(f"Found {len(posts)} posts via HTML")
        return pd.DataFrame(posts)

    except Exception as e:
        print(f"Reddit scraping failed: {str(e)}")
        return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Scrape Trustpilot reviews with robust selectors"""
    print(f"Attempting to scrape Trustpilot for: {keyword}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        url = f"https://www.trustpilot.com/search?query={keyword}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        
        # Updated selectors
        for card in soup.select('[data-service-review]')[:max_reviews]:
            try:
                text = card.select_one('[data-service-review-text]').get_text(strip=True)
                date = card.select_one('time').get('datetime', '')
                reviews.append({
                    'comment': text,
                    'source': 'Trustpilot',
                    'date': pd.to_datetime(date) if date else datetime.now()
                })
                time.sleep(random.uniform(0.5, 2))  # Respectful delay
            except Exception as e:
                print(f"Skipping review due to: {str(e)}")
                continue
        
        print(f"Found {len(reviews)} Trustpilot reviews")
        return pd.DataFrame(reviews)
        
    except Exception as e:
        print(f"Trustpilot scraping failed: {str(e)}")
        return pd.DataFrame()
