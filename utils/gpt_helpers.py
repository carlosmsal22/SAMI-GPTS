
import os
import csv
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_PATH = "logs/gpt_logs.csv"

def run_gpt_prompt(prompt: str, model="gpt-4", temperature=0.7, max_tokens=750, module="brand_reputation"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful market research assistant specializing in brand reputation analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content.strip()
        log_conversation(module, prompt, reply)
        return reply
    except Exception as e:
        return f"❌ GPT Error: {e}"

def log_conversation(module, prompt, response):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, module, prompt, response])
