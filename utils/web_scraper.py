from typing import List, Dict
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser
import urllib.parse


def scrape_reddit_cybersecurity(company: str) -> List[Dict]:
    query = f"site:reddit.com {company} cybersecurity"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.select("div.g"):
        title_el = g.select_one("h3")
        link_el = g.select_one("a")
        if title_el and link_el:
            results.append({
                "comment": title_el.text.strip(),
                "url": link_el['href'],
                "date": datetime.now().strftime("%Y-%m-%d")
            })

    return results


def scrape_google_news_rss(company: str) -> List[Dict]:
    rss_url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(rss_url)

    results = []
    for entry in feed.entries[:10]:
        results.append({
            "title": entry.title,
            "url": entry.link,
            "date": entry.published if 'published' in entry else datetime.now().strftime("%Y-%m-%d")
        })

    return results
