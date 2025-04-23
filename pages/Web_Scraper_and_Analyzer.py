import streamlit as st
import pandas as pd
from utils.web_scraper_helpers import scrape_reddit_cybersecurity as scrape_reddit
from utils.gpt_helpers import run_gpt_prompt
import sys
from pathlib import Path
from datetime import datetime

# Configure paths
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(page_title="Enterprise Analyzer", layout="wide")
    st.title("🔍 Enterprise Reputation Analyzer")
    
    # Input Section
    company = st.text_input("Enter company name", "Secureonix")
    num = st.slider("Number of posts/reviews", 5, 50, 10)
    
    if st.button("🔍 Collect Data"):
        with st.spinner(f"Gathering data about {company}..."):
            try:
                reddit_df = scrape_reddit(company, max_posts=num)
                trust_df = scrape_trustpilot(company, max_reviews=num)
                
                # Combine data
                dfs = []
                for df in [reddit_df, trust_df]:
                    if not df.empty:
                        if 'title' in df.columns:  # Reddit uses 'title'
                            df = df.rename(columns={'title': 'comment'})
                        dfs.append(df)
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.company_data = full_df
                    st.success(f"✅ Found {len(full_df)} mentions!")
                    
                    with st.expander("View Data"):
                        st.dataframe(full_df)
                else:
                    st.warning("No data found. Try different company naming.")
                    
            except Exception as e:
                st.error(f"Data collection failed: {str(e)}")

    # Analysis Section
    if 'company_data' in st.session_state:
        st.divider()
        st.subheader("AI Analysis")
        
        if st.button("🤖 Generate Report"):
            df = st.session_state.company_data
            
            # Prepare prompt
            prompt = f"""Analyze {company}'s reputation based on:
            
            **Comments:**
            {df['comment'].str.cat(sep='\n- ')[:3000]}
            
            **Provide:**
            1. Sentiment score (1-10)
            2. Top 3 positive aspects
            3. Top 3 complaints
            4. 50-word summary"""
            
            with st.spinner("Analyzing..."):
                analysis = run_gpt_prompt(prompt)
                st.markdown("## 📊 Analysis Report")
                st.write(analysis)

if __name__ == "__main__":
    main()
