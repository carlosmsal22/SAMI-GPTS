import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def hybrid_scrape(company: str) -> List[Dict]:
    """Enhanced scraper for SAMI compatibility"""
    sources = {
        'Trustpilot': lambda: scrape_trustpilot(company),
        'Reddit': lambda: scrape_reddit_cybersecurity(company),
        'News': lambda: scrape_google_news_rss(company)
    }
    
    results = []
    for name, scraper in sources.items():
        try:
            data = scraper()
            results.extend([{
                "content": d.get('comment', d.get('title', '')),
                "source": name,
                "date": d.get('date', datetime.now().strftime('%Y-%m-%d')),
                "url": d.get('url', '')
            } for d in data])
        except Exception as e:
            print(f"{name} scrape failed: {e}")
    
    return [
        d for d in results 
        if len(d['content']) > 30  # SAMI quality threshold
    ][:50]  # Limit to top 50 mentions
