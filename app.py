import sys
import os
from pathlib import Path

# Add the parent directory to Python path (GitHub-specific fix)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    from utils.gpt_helpers import run_gpt_prompt
    from utils.web_scraper import scrape_reddit, scrape_trustpilot
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.error("Current working directory: " + os.getcwd())
    st.error("Directory contents: " + ", ".join(os.listdir()))
    if os.path.exists('utils'):
        st.error("Utils contents: " + ", ".join(os.listdir('utils')))
    else:
        st.error("Utils directory does not exist!")
    raise

import streamlit as st

st.set_page_config(page_title="SAMI GPT Suite", layout="wide")
st.title("SAMI GPT Suite")
st.markdown("Welcome to the **SAMI.AI GPT Suite**. Please choose a module from the sidebar to begin your insights journey.")
st.sidebar.success("Select a module from the sidebar.")
