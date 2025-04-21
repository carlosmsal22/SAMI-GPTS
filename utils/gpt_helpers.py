
import os
import openai

# Initialize OpenAI client with v1-style call
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_gpt(prompt_config, user_input):
    messages = [{"role": "system", "content": prompt_config.get("instructions", "")}]
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
