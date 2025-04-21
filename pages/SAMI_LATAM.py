
import streamlit as st
from utils.gpt_helpers import run_gpt
import json

st.set_page_config(layout="wide")
st.title("🌎 SAMI.AI INSIGHTS LATAM")
st.write("Upload a dataset or enter a prompt to get started.")

uploaded_file = st.file_uploader("Upload file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])

# Load prompt config
with open("prompts/SAMI_AI_INSIGHTS_LATAM_Enhanced.json", "r") as f:
    prompt = json.load(f)

# Text input with prefilled capability
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

def insert_suggestion(text):
    st.session_state.prompt_input = text

st.text_area("Or enter your prompt here:", key="prompt_input", height=200)

# Clickable suggestions
if prompt.get("prompt_suggestions"):
    st.markdown("### 💡 Prompt Suggestions")
    for i, suggestion in enumerate(prompt["prompt_suggestions"]):
        if st.button("🖋️ {}".format(suggestion), key="suggestion_{}".format(i)):
            st.session_state.prompt_input = suggestion

# Run button
if st.button("Run Analysis"):
    if st.session_state.prompt_input:
        result = run_gpt(prompt, st.session_state.prompt_input)
        st.markdown("### 🔍 GPT Response")
        st.write(result)
    else:
        st.warning("Please enter a prompt to begin.")
