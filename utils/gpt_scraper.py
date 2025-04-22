import openai
import os
from typing import List, Dict

class EnterpriseScraper:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def scrape_enterprise_data(self, company: str) -> List[Dict]:
        """Leverage your custom GPT's scraping capabilities"""
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",  # Your custom model name
            messages=[{
                "role": "user",
                "content": f"""
                SCRAPING INSTRUCTIONS:
                1. Perform comprehensive search for {company}
                2. Cover: News, Social, Reviews, Forums
                3. Return as JSON with:
                   - content (string)
                   - source (string)
                   - date (string)
                   - sentiment (1-10)
                """
            }],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)['results']

    def analyze_sentiment(self, data: List[Dict]) -> Dict:
        """Multi-dimensional sentiment analysis"""
        analysis = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{
                "role": "user",
                "content": f"""
                ANALYZE THIS ENTERPRISE DATA:
                {json.dumps(data)}
                
                RETURN JSON WITH:
                - overall_score (1-10)
                - by_source: {{source: score}}
                - strengths (list)
                - weaknesses (list)
                - crisis_alerts (list)
                """
            }],
            response_format={ "type": "json_object" }
        )
        return json.loads(analysis.choices[0].message.content)