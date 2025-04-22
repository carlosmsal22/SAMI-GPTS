import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

def get_google_news_rss(company_name, max_results=10):
    """Scrape Google News RSS with enhanced parsing"""
    try:
        url = f"https://news.google.com/rss/search?q={company_name}+stock&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'xml')
        
        articles = []
        for item in soup.find_all('item')[:max_results]:
            source = item.find('source').text if item.find('source') else 'Google News'
            articles.append({
                'content': item.title.text,
                'source': source,
                'date': item.pubDate.text,
                'type': 'news',
                'url': item.link.text
            })
        return articles
    except Exception as e:
        print(f"Google News RSS failed: {e}")
        return []

def scrape_nitter_twitter(company_name, max_results=10):
    """Scrape Twitter via Nitter with retries"""
    try:
        url = f"https://nitter.net/search?q={company_name}&f=tweets"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tweets = []
        for tweet in soup.select('.tweet-content')[:max_results]:
            tweets.append({
                'content': tweet.get_text(strip=True),
                'source': 'Twitter',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': 'social',
                'url': f"https://twitter.com{i/tweet.find_parent('a')['href']}" if tweet.find_parent('a') else ''
            })
        return tweets
    except Exception as e:
        print(f"Nitter failed: {e}")
        return []

def scrape_reddit_enterprise(company_name, max_results=10):
    """Scrape Reddit with enhanced error handling"""
    try:
        url = f"https://www.reddit.com/search.json?q={company_name}&limit={max_results}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            posts.append({
                'content': post['data']['title'],
                'source': 'Reddit',
                'date': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%d'),
                'type': 'forum',
                'url': f"https://reddit.com{post['data']['permalink']}"
            })
        return posts
    except Exception as e:
        print(f"Reddit failed: {e}")
        return []

def hybrid_scrape(company_name, max_results=15):
    """Combined scraper with failover logic"""
    sources = [
        get_google_news_rss,
        scrape_nitter_twitter, 
        scrape_reddit_enterprise
    ]
    
    all_results = []
    for source in sources:
        try:
            results = source(company_name, max_results//len(sources))
            if results:
                all_results.extend(results)
                time.sleep(random.uniform(1, 3))  # Be polite
        except Exception as e:
            print(f"Source {source.__name__} failed: {e}")
    
    return pd.DataFrame(all_results).drop_duplicates('content')