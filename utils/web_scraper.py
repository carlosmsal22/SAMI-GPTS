import pandas as pd
import praw  # For Reddit API
import requests  # For Trustpilot scraping
from bs4 import BeautifulSoup

def scrape_reddit(keyword, max_posts=10):
    """
    Scrape Reddit posts containing the keyword
    Returns DataFrame with columns: ['comment', 'source', 'date']
    """
    # Initialize Reddit API (configure with your credentials)
    reddit = praw.Reddit(
        client_id='your_client_id',
        client_secret='your_client_secret',
        user_agent='your_user_agent'
    )
    
    comments = []
    for submission in reddit.subreddit('all').search(keyword, limit=max_posts):
        comments.append({
            'comment': submission.title,
            'source': 'Reddit',
            'date': submission.created_utc
        })
    
    return pd.DataFrame(comments)

def scrape_trustpilot(keyword, max_reviews=10):
    """
    Scrape Trustpilot reviews for the given brand
    Returns DataFrame with columns: ['comment', 'source', 'date']
    """
    url = f"https://www.trustpilot.com/search?query={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews = []
    for review in soup.select('.review-content', limit=max_reviews):
        reviews.append({
            'comment': review.select_one('.review-content__text').text.strip(),
            'source': 'Trustpilot',
            'date': review.select_one('.review-content-header__dates').text.strip()
        })
    
    return pd.DataFrame(reviews)
