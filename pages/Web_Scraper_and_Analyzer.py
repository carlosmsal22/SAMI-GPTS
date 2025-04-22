import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt
import sys
from pathlib import Path
import time

# Configure paths
sys.path.append(str(Path(__file__).parent))

# Debug settings
DEBUG = True
MAX_RETRIES = 2

def display_debug_info(reddit_df, trust_df):
    """Helper to show debugging information"""
    with st.expander("Debug Information"):
        st.write("Reddit Data:")
        if not reddit_df.empty:
            st.dataframe(reddit_df)
            st.write(f"Reddit columns: {list(reddit_df.columns)}")
        else:
            st.warning("No Reddit data")
        
        st.write("Trustpilot Data:")
        if not trust_df.empty:
            st.dataframe(trust_df)
            st.write(f"Trustpilot columns: {list(trust_df.columns)}")
        else:
            st.warning("No Trustpilot data")

def main():
    st.set_page_config(page_title="Brand Analyzer", layout="wide")
    st.title("🔍 Modern Brand Reputation Analyzer")
    
    # Input Section
    keyword = st.text_input("Enter a brand name (e.g. Nike, Starbucks)", 
                          help="Try popular brands first for better results")
    num = st.slider("Number of posts/reviews", 5, 50, 10, 
                   help="More samples may take longer but provide better analysis")
    
    # Scraping Section
    if st.button("🔎 Scrape Brand Data", type="primary"):
        if not keyword.strip():
            st.warning("Please enter a valid brand name")
            return
            
        with st.spinner(f"Gathering data about {keyword}..."):
            reddit_df = pd.DataFrame()
            trust_df = pd.DataFrame()
            
            # Retry logic
            for attempt in range(MAX_RETRIES):
                try:
                    if reddit_df.empty:
                        reddit_df = scrape_reddit(keyword, max_posts=num)
                    if trust_df.empty:
                        trust_df = scrape_trustpilot(keyword, max_reviews=num)
                    
                    if not reddit_df.empty or not trust_df.empty:
                        break
                        
                except Exception as e:
                    st.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(2)  # Wait before retry
            
            # Process results
            if DEBUG:
                display_debug_info(reddit_df, trust_df)
            
            if reddit_df.empty and trust_df.empty:
                st.error("""
                ⚠️ No data found. This could be because:
                - The brand isn't discussed on these platforms
                - Temporary scraping limitations
                - Try a more popular brand name
                """)
                return
                
            # Standardize data
            dfs = []
            for df, source in [(reddit_df, "Reddit"), (trust_df, "Trustpilot")]:
                if not df.empty:
                    # Find comment column (handles different names)
                    comment_col = next(
                        (col for col in df.columns 
                         if any(word in col.lower() for word in ['comment', 'text', 'title', 'review']),
                        None  # Default value if no match found
                    )
                    if comment_col:
                        df = df.rename(columns={comment_col: 'comment'})
                        dfs.append(df)
            
            if dfs:
                full_df = pd.concat(dfs, ignore_index=True)
                st.session_state.scraped_data = full_df
                
                st.success(f"✅ Found {len(full_df)} comments!")
                st.dataframe(full_df.head())
                
                # Show quick stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Comments", len(full_df))
                with col2:
                    st.metric("Sources", ", ".join(full_df['source'].unique()))
            else:
                st.error("No valid comments found in the scraped data")

    # Analysis Section
    if "scraped_data" in st.session_state:
        st.divider()
        st.subheader("AI Analysis")
        
        if st.button("🤖 Analyze with AI", type="primary"):
            df = st.session_state.scraped_data
            
            if df.empty:
                st.warning("No data to analyze")
                return
                
            comments = df['comment'].dropna().str.strip()
            comments = comments[comments != ""]  # Remove empty strings
            
            if len(comments) == 0:
                st.warning("No valid comments for analysis")
                return
                
            # Build better prompt
            prompt = f"""Analyze brand sentiment for {keyword} based on these user comments:

1. Overall Sentiment (Positive/Neutral/Negative)
2. Top 3 Positive Aspects Mentioned
3. Top 3 Complaints or Issues
4. 50-word Reputation Summary
5. Suggested Improvements

Comments:
""" + "\n".join(f"- {c[:300]}" for c in comments.head(10))  # Truncate long comments

            st.code(prompt)
            
            with st.spinner("Analyzing with AI..."):
                try:
                    response = run_gpt_prompt(
                        prompt,
                        model="gpt-4",
                        temperature=0.7,
                        max_tokens=500
                    )
                    st.success("Analysis Complete!")
                    st.markdown("## 📊 Brand Reputation Report")
                    st.markdown(response)
                    
                    # Export option
                    if st.button("💾 Save Report"):
                        from datetime import datetime
                        filename = f"{keyword}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                        with open(filename, 'w') as f:
                            f.write(response)
                        st.success(f"Saved as {filename}")
                        
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    if DEBUG:
                        st.exception(e)

if __name__ == "__main__":
    main()
