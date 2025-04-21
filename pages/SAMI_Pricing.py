
import streamlit as st
from utils.gpt_helpers import run_gpt
import json

st.set_page_config(layout="wide")
st.title("💰 SAMI Pricing AI")
st.write("Upload a dataset or enter a prompt for pricing analysis.")

uploaded_file = st.file_uploader("Upload file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])
user_input = st.text_area("Or enter your prompt here:", height=200)

if st.button("Run Analysis"):
    if user_input:
        with open("prompts/SAMI_Pricing_AI_Finalized.json", "r") as f:
            prompt = json.load(f)
        result = run_gpt(prompt, user_input)
        st.markdown("### 🔍 GPT Response")
        st.write(result)
    else:
        st.warning("Please enter a prompt to begin.")
