# utils/gpt_helpers.py (OpenAI SDK v1.0+)
import openai
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_gpt_prompt(prompt: str, model="gpt-4", temperature=0.7, max_tokens=750):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful market research assistant specializing in brand reputation analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT Error: {e}"
