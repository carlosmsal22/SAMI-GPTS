import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_cybersecurity_forums(keyword, max_posts=10):
    """Scrape cybersecurity discussion forums"""
    try:
        # Scrape Reddit's netsec and cybersecurity channels
        url = f"https://www.reddit.com/r/cybersecurity/search.json?q={keyword}&limit={max_posts}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()['data']['children']
        
        posts = [{
            'comment': post['data']['title'],
            'source': 'Reddit',
            'date': datetime.fromtimestamp(post['data']['created_utc']),
            'url': f"https://reddit.com{post['data']['permalink']}"
        } for post in data]
        
        return pd.DataFrame(posts)
    except Exception as e:
        print(f"Forum scraping error: {e}")
        return pd.DataFrame()

def scrape_tech_review_sites(keyword, max_reviews=10):
    """Scrape G2 Crowd and other tech review sites"""
    try:
        # Scrape G2 Crowd (popular for enterprise software)
        url = f"https://www.g2.com/products/{keyword.lower().replace(' ', '-')}/reviews"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reviews = []
        for review in soup.select('.review-card')[:max_reviews]:
            reviews.append({
                'comment': review.select_one('.review-body').get_text(strip=True),
                'source': 'G2 Crowd',
                'date': review.select_one('time').get('datetime'),
                'rating': len(review.select('.star-rating .filled'))
            })
            time.sleep(1)  # Be polite
            
        return pd.DataFrame(reviews)
    except Exception as e:
        print(f"Review site error: {e}")
        return pd.DataFrame()

def scrape_news_mentions(keyword, max_articles=5):
    """Scrape tech news mentions"""
    try:
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey=YOUR_API_KEY"
        response = requests.get(url, timeout=10)
        articles = response.json()['articles'][:max_articles]
        
        return pd.DataFrame([{
            'comment': article['title'],
            'source': article['source']['name'],
            'date': article['publishedAt'],
            'url': article['url']
        } for article in articles])
    except Exception as e:
        print(f"News scraping error: {e}")
        return pd.DataFrame()
