
# utils/gpt_helpers.py
import openai

# Make sure to set your OpenAI API key in the environment or use Streamlit secrets
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_gpt_prompt(prompt: str, model="gpt-4", temperature=0.7, max_tokens=750):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful market research assistant specializing in brand reputation analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ GPT Error: {e}"
