
import streamlit as st
from utils.gpt_helpers import run_gpt
import json

st.set_page_config(layout="wide")
st.title("💰 SAMI Pricing AI")
st.write("Upload a dataset or enter a prompt to get started.")

uploaded_file = st.file_uploader("Upload file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])

# Load prompt config
with open("prompts/SAMI_Pricing_AI_Finalized.json", "r") as f:
    prompt = json.load(f)

if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

if "suggested_prompt" in st.session_state:
    st.session_state.prompt_input = st.session_state.suggested_prompt
    del st.session_state["suggested_prompt"]

st.text_area("Or enter your prompt here:", key="prompt_input", height=200)

if prompt.get("prompt_suggestions"):
    st.markdown("### 💡 Prompt Suggestions")
    for i, suggestion in enumerate(prompt["prompt_suggestions"]):
        if st.button(f"🖋️ {suggestion}", key=f"suggestion_{i}"):
            st.session_state.suggested_prompt = suggestion
            st.rerun()

if st.button("Run Analysis"):
    if st.session_state.prompt_input:
        result = run_gpt(prompt, st.session_state.prompt_input)
        st.markdown("### 🔍 GPT Response")
        st.write(result)
    else:
        st.warning("Please enter a prompt to begin.")
