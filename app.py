import sys
import os
from pathlib import Path
import streamlit as st  # Must import streamlit FIRST

# Configure page settings early
st.set_page_config(page_title="SAMI GPT Suite", layout="wide")

# Now set up path and imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    from utils.gpt_helpers import run_gpt_prompt
    from utils.web_scraper import scrape_reddit, scrape_trustpilot
except ImportError as e:
    # Now we can use st since it's imported
    st.error(f"Import Error: {str(e)}")
    st.error(f"Current directory: {os.getcwd()}")
    st.error(f"Directory contents: {os.listdir()}")
    
    if os.path.exists('utils'):
        st.error(f"Utils contents: {os.listdir('utils')}")
    else:
        st.error("Utils directory not found!")
    
    # Create a debug expander
    with st.expander("Debug Info"):
        st.write("System Path:")
        st.write(sys.path)
        
        st.write("File Structure:")
        st.code("""
        AMI-GPTS/
        ├── utils/
        │   ├── __init__.py
        │   ├── gpt_helpers.py
        │   └── web_scraper.py
        ├── app.py
        """)
    raise

# Rest of your app
st.title("SAMI GPT Suite")
st.markdown("Welcome to the **SAMI.AI GPT Suite**. Please choose a module from the sidebar to begin your insights journey.")
st.sidebar.success("Select a module from the sidebar.")
