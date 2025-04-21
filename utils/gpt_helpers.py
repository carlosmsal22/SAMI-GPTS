
import openai
import json

def load_prompt(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def run_gpt(prompt_config, user_input, model="gpt-4"):
    messages = [
        {"role": "system", "content": prompt_config["instructions"]},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message["content"]
