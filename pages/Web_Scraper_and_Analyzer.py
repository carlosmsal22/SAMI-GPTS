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
                          value="Apple",  # Default to Apple for testing
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
                    st.write("Reddit Data Shape:", reddit_df.shape)
                    st.write("Trustpilot Data Shape:", trust_df.shape)
                    if not reddit_df.empty:
                        st.write("Sample Reddit Comments:", reddit_df['comment'].head().tolist())
                    if not trust_df.empty:
                        st.write("Sample Trustpilot Comments:", trust_df['comment'].head().tolist())
                
                # Process data
                dfs = []
                for df, source in [(reddit_df, "Reddit"), (trust_df, "Trustpilot")]:
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
                    
                    # Show success metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Comments", len(full_df))
                    with col2:
                        st.metric("Sources", ", ".join(full_df['source'].unique()))
                else:
                    st.error("""
                    No data found. This could be because:
                    - The brand isn't listed on Trustpilot
                    - No recent Reddit discussions
                    - Temporary scraping limitations
                    """)
                    
            except Exception as e:
                st.error(f"Scraping failed: {str(e)}")
                st.info("Try again later or with a different brand")

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
2. Key Positive Aspects (3 bullet points)
3. Main Complaints (3 bullet points)
4. Reputation Summary (50 words)
5. Improvement Suggestions (3 actionable items)

Comments:
""" + "\n".join(f"- {c[:200]}..." for c in comments)

                    with st.spinner("Analyzing with AI..."):
                        try:
                            response = run_gpt_prompt(
                                prompt,
                                model="gpt-4",
                                temperature=0.7,
                                max_tokens=600
                            )
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
