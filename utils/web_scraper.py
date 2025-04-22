import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

def scrape_reddit(keyword, max_posts=10):
    """Reliable Reddit scraper using alternative methods"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Method 1: Use Reddit's JSON API
        url = f"https://www.reddit.com/search.json?q={keyword}&limit={max_posts}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()['data']['children']
        if data:
            return pd.DataFrame([{
                'comment': post['data']['title'],
                'source': 'Reddit',
                'date': datetime.fromtimestamp(post['data']['created_utc']),
                'url': f"https://reddit.com{post['data']['permalink']}"
            } for post in data])
        
        # Method 2: Fallback to RSS
        rss_url = f"https://www.reddit.com/search.rss?q={keyword}&limit={max_posts}"
        response = requests.get(rss_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'xml')
        
        posts = [{
            'comment': item.title.text,
            'source': 'Reddit',
            'date': datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %Z'),
            'url': item.link.text
        } for item in soup.find_all('item')[:max_posts]]
        
        return pd.DataFrame(posts)
        
    except Exception as e:
        print(f"Reddit scraping failed: {e}")
        return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Reliable Trustpilot scraper with modern selectors"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        # Search for business page
        search_url = f"https://www.trustpilot.com/search?query={keyword}"
        response = requests.get(search_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find business unit card
        business_card = soup.find('div', {'class': 'business-unit-card'})
        if not business_card:
            return pd.DataFrame()
            
        # Get reviews URL
        reviews_path = business_card.find('a')['href']
        reviews_url = f"https://www.trustpilot.com{reviews_path}"
        time.sleep(2)  # Be polite
        
        # Scrape reviews
        response = requests.get(reviews_url, headers=headers, timeout=20)
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
                
        return pd.DataFrame(reviews)
        
    except Exception as e:
        print(f"Trustpilot scraping failed: {e}")
        return pd.DataFrame()
