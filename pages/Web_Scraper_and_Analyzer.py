import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt

st.title("🧠 Scrape + Analyze Brand Reputation")

keyword = st.text_input("Enter a brand (e.g. Secureonix)")
num = st.slider("How many posts/reviews?", 5, 50, 10)

if st.button("Scrape the Web"):
    with st.spinner("Scraping data..."):
        reddit_df = scrape_reddit(keyword, max_posts=num)
        trust_df = scrape_trustpilot(keyword, max_reviews=num)
        
        # Check if data was returned and has the expected columns
        dfs = []
        for df, source in [(reddit_df, "Reddit"), (trust_df, "Trustpilot")]:
            if not df.empty:
                # Standardize column names
                if 'title' in df.columns:  # Reddit returns 'title' instead of 'comment'
                    df = df.rename(columns={'title': 'comment'})
                if 'comment' in df.columns:
                    dfs.append(df)
                else:
                    st.warning(f"No comments found in {source} data")
        
        if dfs:
            full_df = pd.concat(dfs, ignore_index=True)
            st.session_state.scraped_data = full_df
            st.success(f"Scraped {len(full_df)} comments! Preview:")
            st.dataframe(full_df)
        else:
            st.error("No valid data found from either source")
            st.session_state.scraped_data = None

if "scraped_data" in st.session_state and st.session_state.scraped_data is not None:
    if st.button("Analyze with GPT"):
        try:
            # Verify data structure
            if 'comment' not in st.session_state.scraped_data.columns:
                st.error("Data format error: No 'comment' column found")
                st.write("Available columns:", st.session_state.scraped_data.columns.tolist())
                return
            
            # Get non-empty comments
            comments = st.session_state.scraped_data['comment'].dropna().head(10)
            
            if len(comments) == 0:
                st.warning("No valid comments found for analysis")
            else:
                # Build prompt
                prompt = (
                    f"Analyze these comments about '{keyword}':\n"
                    "1. Overall sentiment (Positive/Negative/Neutral)\n"
                    "2. Key positive aspects\n"
                    "3. Main complaints\n"
                    "4. Brand reputation summary\n\n"
                    "Comments:\n" + 
                    "\n".join(f"- {c}" for c in comments)
                )
                
                st.markdown("### ✅ Prompt Sent to GPT")
                st.code(prompt)

                with st.spinner("Analyzing..."):
                    response = run_gpt_prompt(prompt, module="brand_reputation")
                
                st.markdown("### 🧠 GPT Response")
                st.write(response)
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
else:
    st.info("Please scrape data first to enable analysis")
