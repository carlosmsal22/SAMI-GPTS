import sys
import os
import pandas as pd
import streamlit as st
from pathlib import Path

# Configure paths
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import utilities
try:
    from utils.gpt_helpers import run_gpt_prompt
    from utils.web_scraper import scrape_reddit, scrape_trustpilot
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.error(f"Current directory: {os.getcwd()}")
    st.error(f"Directory contents: {os.listdir()}")
    if os.path.exists('utils'):
        st.error(f"Utils contents: {os.listdir('utils')}")
    else:
        st.error("Utils directory not found!")
    raise

# App configuration
st.set_page_config(page_title="SAMI GPT Suite", layout="wide")
st.title("🧠 Scrape + Analyze Brand Reputation")

# Main app
keyword = st.text_input("Enter a brand (e.g. Secureonix)")
num = st.slider("How many posts/reviews?", 5, 50, 10)

if st.button("Scrape the Web"):
    try:
        with st.spinner("Scraping data..."):
            reddit_df = scrape_reddit(keyword, max_posts=num)
            trust_df = scrape_trustpilot(keyword, max_reviews=num)
            
            # Validate and combine data
            dfs = []
            if not reddit_df.empty and 'comment' in reddit_df.columns:
                dfs.append(reddit_df)
            if not trust_df.empty and 'comment' in trust_df.columns:
                dfs.append(trust_df)
            
            if dfs:
                full_df = pd.concat(dfs, ignore_index=True)
                st.session_state.scraped_data = full_df
                st.success(f"Scraped {len(full_df)} comments! Preview:")
                st.dataframe(full_df.head())
            else:
                st.error("No valid data found")
                st.session_state.scraped_data = None
                
    except Exception as e:
        st.error(f"Scraping failed: {str(e)}")
        st.session_state.scraped_data = None

# Analysis section
if "scraped_data" in st.session_state and st.session_state.scraped_data is not None:
    if st.button("Analyze with GPT"):
        try:
            comments = st.session_state.scraped_data['comment'].dropna().head(10)
            if len(comments) == 0:
                st.warning("No valid comments found")
            else:
                prompt = f"Analyze sentiment for '{keyword}' based on these comments:\n\n"
                prompt += "\n".join([f"- {comment}" for comment in comments])
                
                st.markdown("### ✅ Prompt Sent to GPT")
                st.code(prompt)

                with st.spinner("Analyzing..."):
                    response = run_gpt_prompt(prompt, module="brand_reputation")
                
                st.markdown("### 🧠 Analysis Results")
                st.write(response)
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
else:
    st.info("Please scrape data first to enable analysis")
