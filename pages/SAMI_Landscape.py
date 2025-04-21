
import streamlit as st
import pandas as pd
import json
from utils.gpt_helpers import run_gpt
from utils.visualizers import plot_bar_chart
from utils.stats_helpers import summarize_dataframe
from utils.export_helpers import export_csv, export_pdf

st.set_page_config(layout="wide")
st.title("🌐 SAMI Landscape AI")
st.write("Upload a dataset or enter a prompt to get started.")

# Upload
uploaded_file = st.file_uploader("Upload file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])
df = None

# Load prompt template
with open("prompts/SAMI_Landscape_AI_Finalized.json", "r") as f:
    prompt = json.load(f)

# Session prompt
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

if "suggested_prompt" in st.session_state:
    st.session_state.prompt_input = st.session_state.suggested_prompt
    del st.session_state["suggested_prompt"]

st.text_area("Or enter your prompt here:", key="prompt_input", height=200)

# Suggestions
if prompt.get("prompt_suggestions"):
    st.markdown("### 💡 Prompt Suggestions")
    for i, suggestion in enumerate(prompt["prompt_suggestions"]):
        if st.button(f"🖋️ {suggestion}", key=f"suggestion_{i}"):
            st.session_state.suggested_prompt = suggestion
            st.rerun()

# Process file
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            df = pd.read_csv(uploaded_file, delimiter="\t")
        st.success(f"Loaded: {uploaded_file.name}")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")

# GPT + chart + exports
if st.button("Run Analysis"):
    if st.session_state.prompt_input:
        user_prompt = st.session_state.prompt_input
        result = run_gpt(prompt, user_prompt)
        st.markdown("### 🔍 GPT Response")
        st.write(result)

        if df is not None:
            st.markdown("### 📊 Data Summary")
            summary_df = summarize_dataframe(df)
            st.dataframe(summary_df)

            num_cols = df.select_dtypes(include='number').columns
            if len(num_cols) > 0:
                x_col = df.columns[0]
                y_col = num_cols[0]
                plot_bar_chart(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            else:
                st.warning("No numeric columns available for visualization.")

            export_csv(summary_df, "summary.csv")
            export_pdf(result, "summary.pdf")
    else:
        st.warning("Please enter a prompt.")
