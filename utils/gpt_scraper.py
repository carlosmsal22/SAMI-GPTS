import openai
import os
import json  # Ensure this import exists
from typing import List, Dict
from datetime import datetime

class EnterpriseScraper:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def scrape_enterprise_data(self, company: str) -> List[Dict]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{
                    "role": "user",
                    "content": f"""
                    Collect enterprise data for {company} from:
                    - News articles
                    - Social media
                    - Industry forums
                    - Review sites
                    
                    Return as JSON with:
                    - content (string)
                    - source (string)
                    - date (string)
                    - sentiment (1-10)
                    """
                }],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            data = json.loads(response.choices[0].message.content)
            return data.get('results', [])
            
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return []

    def analyze_sentiment(self, data: List[Dict]) -> Dict:
        try:
            analysis = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{
                    "role": "user",
                    "content": f"""
                    Analyze this enterprise data:
                    {json.dumps(data)}
                    
                    Return JSON with:
                    - overall_score (1-10)
                    - sentiment_score (1-10)
                    - top_strengths (list)
                    - top_weaknesses (list)
                    - crisis_alerts (list)
                    - growth_potential (1-10)
                    """
                }],
                response_format={"type": "json_object"}
            )
            return json.loads(analysis.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
