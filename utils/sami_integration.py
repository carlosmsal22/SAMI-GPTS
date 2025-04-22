import json
import openai
from typing import Dict, List
from datetime import datetime

class SAMIAnalyzer:
    def __init__(self):
        self.config = {
            "title": "SAMI Brand & Reputation AI",
            "instructions": "...",  # Your existing instructions
            "prompt_suggestions": [...]  # Your existing suggestions
        }
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_report(self, scraped_data: List[Dict], analysis_type: str) -> Dict:
        """Generate SAMI-style reports from scraped data"""
        prompt = self._build_sami_prompt(scraped_data, analysis_type)
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return self._format_sami_output(json.loads(response.choices[0].message.content))

    def _build_sami_prompt(self, data: List[Dict], analysis_type: str) -> str:
        """Construct SAMI-compatible prompt"""
        base = self.config['instructions']
        examples = "\n".join(f"- {d['content'][:100]}..." for d in data[:5])
        
        return f"""
        {base}
        
        ANALYSIS REQUEST: {analysis_type}
        DATA SAMPLE:
        {examples}
        
        RESPONSE FORMAT:
        {{
            "overview": "strategic_summary",
            "sentiment_breakdown": {{"positive": %, "negative": %, "neutral": %}},
            "emotional_analysis": ["emotion": strength],
            "competitive_benchmark": "text",
            "strategic_recommendations": ["list"]
        }}
        """

    def _format_sami_output(self, raw: Dict) -> Dict:
        """Ensure SAMI branding in output"""
        return {
            "title": self.config['title'],
            "timestamp": datetime.now().isoformat(),
            "analysis": raw,
            "visual_metaphors": [
                "chess_piece" if raw.get('sentiment_breakdown', {}).get('positive', 0) > 60 else "warning_sign",
                "thermometer" if any(e['emotion'] == 'frustration' for e in raw.get('emotional_analysis', [])) else "sun"
            ]
        }