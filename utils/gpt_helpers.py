
import json
import openai

def load_prompt_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def run_gpt_analysis(prompt, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
