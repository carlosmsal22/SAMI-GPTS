# Add this at the top of app.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.gpt_helpers import run_gpt_prompt
from utils.web_scraper import scrape_reddit, scrape_trustpilot
import streamlit as st

st.set_page_config(page_title="SAMI GPT Suite", layout="wide")

st.title("SAMI GPT Suite")
st.markdown("Welcome to the **SAMI.AI GPT Suite**. Please choose a module from the sidebar to begin your insights journey.")

st.sidebar.success("Select a module from the sidebar.")
