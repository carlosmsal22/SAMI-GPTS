
import os
import openai
import streamlit as st

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_gpt(prompt_config, user_input):
    # Setup system instruction
    messages = [{"role": "system", "content": prompt_config.get("instructions", "")}]

    # Add memory from prior interaction if available
    history = st.session_state.get("gpt_memory", [])
    messages.extend(history)

    # Append user input
    messages.append({"role": "user", "content": user_input})

    # Run GPT call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    result = response.choices[0].message.content

    # Save message history for chaining
    messages.append({"role": "assistant", "content": result})
    st.session_state["gpt_memory"] = messages[-6:]  # limit memory to last 3 exchanges

    return result
