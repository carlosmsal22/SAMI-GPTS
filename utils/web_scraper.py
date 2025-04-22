import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt

st.title("🧠 Scrape + Analyze Brand Reputation")

keyword = st.text_input("Enter a brand (e.g. Secureonix)")
num = st.slider("How many posts/reviews?", 5, 50, 10)

if st.button("Scrape the Web"):
    try:
        with st.spinner("Scraping data..."):
            reddit_df = scrape_reddit(keyword, max_posts=num)
            trust_df = scrape_trustpilot(keyword, max_reviews=num)
            
            # Validate scraped data
            if reddit_df.empty and trust_df.empty:
                st.error("No data found from either source")
                st.session_state.scraped_data = None
            else:
                # Ensure consistent column names
                required_columns = ['comment']  # Add others if needed
                
                # Check if all required columns exist in both DataFrames
                dfs = []
                if not reddit_df.empty:
                    if all(col in reddit_df.columns for col in required_columns):
                        dfs.append(reddit_df)
                    else:
                        st.error("Reddit data missing required columns")
                
                if not trust_df.empty:
                    if all(col in trust_df.columns for col in required_columns):
                        dfs.append(trust_df)
                    else:
                        st.error("Trustpilot data missing required columns")
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.scraped_data = full_df
                    st.success(f"Scraped {len(full_df)} comments! Preview:")
                    st.dataframe(full_df.head())
                else:
                    st.session_state.scraped_data = None
                    
    except Exception as e:
        st.error(f"Scraping failed: {str(e)}")
        st.session_state.scraped_data = None

# GPT Analysis Section
if "scraped_data" in st.session_state and st.session_state.scraped_data is not None:
    if st.button("Analyze with GPT"):
        try:
            # Validate data before analysis
            if st.session_state.scraped_data.empty:
                st.warning("No data available for analysis")
            elif 'comment' not in st.session_state.scraped_data.columns:
                st.error("Data format error: Missing 'comment' column")
            else:
                # Get non-empty comments
                comments = st.session_state.scraped_data['comment'].dropna().head(10)
                
                if len(comments) == 0:
                    st.warning("No valid comments found for analysis")
                else:
                    # Build prompt
                    prompt = f"Analyze sentiment and brand reputation for '{keyword}' based on these comments:\n\n"
                    prompt += "\n".join([f"- {comment}" for comment in comments])
                    
                    st.markdown("### ✅ Prompt Sent to GPT")
                    st.code(prompt)

                    with st.spinner("Getting GPT analysis..."):
                        response = run_gpt_prompt(prompt, module="brand_reputation")
                    
                    st.markdown("### 🧠 GPT Response")
                    st.write(response)
                    
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
else:
    st.info("Scrape data first to enable analysis")
