import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt
import sys
from pathlib import Path
from datetime import datetime

# Configure paths
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(page_title="Brand Analyzer", layout="wide")
    st.title("🔍 Modern Brand Reputation Analyzer")
    
    # Input Section
    keyword = st.text_input("Enter a brand name (e.g. Nike, Starbucks)", 
                          value="nike",  # Default value for testing
                          help="Try popular brands first for better results")
    num = st.slider("Number of posts/reviews", 5, 50, 10)
    
    # Scraping Section
    if st.button("🔎 Scrape Brand Data", type="primary"):
        if not keyword.strip():
            st.warning("Please enter a valid brand name")
            st.stop()
            
        with st.spinner(f"Gathering data about {keyword}..."):
            try:
                reddit_df = scrape_reddit(keyword, max_posts=num)
                trust_df = scrape_trustpilot(keyword, max_reviews=num)
                
                # Debug preview
                with st.expander("Raw Data Preview"):
                    st.write("Reddit Data:", reddit_df)
                    st.write("Trustpilot Data:", trust_df)
                
                # Process data
                dfs = []
                for df in [reddit_df, trust_df]:
                    if not df.empty:
                        # Standardize column names
                        if 'title' in df.columns:  # Reddit uses 'title'
                            df = df.rename(columns={'title': 'comment'})
                        dfs.append(df)
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.scraped_data = full_df
                    st.success(f"✅ Found {len(full_df)} comments!")
                    st.dataframe(full_df[['comment', 'source']].head())
                else:
                    st.error("No data found. Try a more popular brand or check if the brand exists on these platforms.")
                    
            except Exception as e:
                st.error(f"Scraping failed: {str(e)}")

    # Analysis Section
    if "scraped_data" in st.session_state:
        st.divider()
        st.subheader("AI Analysis")
        
        if st.button("🤖 Analyze with AI", type="primary"):
            df = st.session_state.scraped_data
            
            if df.empty:
                st.warning("No data to analyze")
            else:
                # Prepare comments
                comments = df['comment'].dropna().str.strip()
                comments = comments[comments != ""].head(10)
                
                if len(comments) == 0:
                    st.warning("No valid comments for analysis")
                else:
                    # Build prompt
                    prompt = f"""Analyze brand sentiment for {keyword} based on these user comments:

1. Overall Sentiment (Positive/Neutral/Negative)
2. Key Positive Aspects
3. Main Complaints
4. Reputation Summary (50 words)
5. Improvement Suggestions

Comments:
""" + "\n".join(f"- {c[:200]}..." for c in comments)

                    with st.spinner("Analyzing with AI..."):
                        try:
                            response = run_gpt_prompt(prompt, model="gpt-4")
                            st.success("Analysis Complete!")
                            st.markdown("## 📊 Brand Reputation Report")
                            st.markdown(response)
                            
                            # Export option
                            if st.button("💾 Save Report"):
                                filename = f"{keyword}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                                with open(filename, 'w') as f:
                                    f.write(response)
                                st.success(f"Saved as {filename}")
                                
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
