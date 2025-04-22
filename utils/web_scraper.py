import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import re

def scrape_reddit(keyword, max_posts=10):
    """Modern Reddit scraper that actually works"""
    print(f"Scraping Reddit for: {keyword}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # New Reddit JSON endpoint
        url = f"https://www.reddit.com/search/.json?q={keyword}&limit={max_posts}"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()['data']['children']
        posts = []
        
        for post in data:
            try:
                posts.append({
                    'comment': post['data']['title'],
                    'source': 'Reddit',
                    'date': datetime.fromtimestamp(post['data']['created_utc']),
                    'url': f"https://reddit.com{post['data']['permalink']}"
                })
            except KeyError:
                continue
        
        print(f"Found {len(posts)} Reddit posts")
        return pd.DataFrame(posts)
        
    except Exception as e:
        print(f"Reddit error: {e}")
        # Fallback to RSS
        try:
            rss_url = f"https://www.reddit.com/search.rss?q={keyword}&limit={max_posts}"
            response = requests.get(rss_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'xml')
            
            posts = []
            for item in soup.find_all('item')[:max_posts]:
                posts.append({
                    'comment': item.title.text,
                    'source': 'Reddit',
                    'date': datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %Z'),
                    'url': item.link.text
                })
            
            print(f"Found {len(posts)} posts via RSS")
            return pd.DataFrame(posts)
            
        except Exception as e:
            print(f"RSS fallback failed: {e}")
            return pd.DataFrame()

def scrape_trustpilot(keyword, max_reviews=10):
    """Working Trustpilot scraper with modern selectors"""
    print(f"Scraping Trustpilot for: {keyword}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        # First get the actual business page
        search_url = f"https://www.trustpilot.com/search?query={keyword}"
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        business_link = soup.find('a', {'class': 'business-unit-card'})
        
        if not business_link:
            print("No business page found")
            return pd.DataFrame()
            
        business_url = "https://www.trustpilot.com" + business_link['href']
        time.sleep(2)  # Be polite
        
        # Now scrape the actual reviews
        review_url = f"{business_url}/reviews"
        response = requests.get(review_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('article.review')[:max_reviews]:
            try:
                text = review.select_one('.review-content__text').get_text(strip=True)
                date = review.select_one('time')['datetime']
                rating = len(review.select('.star-rating img[alt*="star"]'))
                
                reviews.append({
                    'comment': text,
                    'source': 'Trustpilot',
                    'date': pd.to_datetime(date),
                    'rating': rating,
                    'url': review_url
                })
                time.sleep(random.uniform(1, 3))  # Random delay
            except Exception as e:
                print(f"Skipping review: {e}")
                continue
        
        print(f"Found {len(reviews)} Trustpilot reviews")
        return pd.DataFrame(reviews)
        
    except Exception as e:
        print(f"Trustpilot error: {e}")
        return pd.DataFrame()
