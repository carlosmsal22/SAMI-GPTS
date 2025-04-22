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
    st.markdown("### Try these guaranteed brands:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍏 Apple"):
            st.session_state.brand = "Apple"
    with col2:
        if st.button("👟 Nike"):
            st.session_state.brand = "Nike"
    
    keyword = st.text_input("Enter a brand name", 
                          value=st.session_state.get('brand', 'Apple'))
    
    num = st.slider("Number of posts/reviews", 5, 50, 10)
    
    # Scraping Section
    if st.button("🔎 Get Brand Data", type="primary"):
        if not keyword.strip():
            st.warning("Please enter a brand name")
            st.stop()
            
        with st.spinner(f"Getting data about {keyword}..."):
            try:
                reddit_df = scrape_reddit(keyword, max_posts=num)
                trust_df = scrape_trustpilot(keyword, max_reviews=num)
                
                # Combine and standardize data
                dfs = []
                for df in [reddit_df, trust_df]:
                    if not df.empty:
                        if 'title' in df.columns:
                            df = df.rename(columns={'title': 'comment'})
                        dfs.append(df)
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.scraped_data = full_df
                    
                    st.success(f"✅ Found {len(full_df)} comments!")
                    with st.expander("View Sample Comments"):
                        st.dataframe(full_df[['comment', 'source']].head())
                        
                    # Show source breakdown
                    st.markdown(f"**Sources:** {', '.join(full_df['source'].unique())}")
                else:
                    st.warning("Showing sample data as fallback")
                    sample_df = pd.DataFrame([
                        {"comment": "Great products but expensive", "source": "Sample"},
                        {"comment": "Excellent customer service", "source": "Sample"}
                    ])
                    st.session_state.scraped_data = sample_df
                    st.dataframe(sample_df)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Analysis Section
    if "scraped_data" in st.session_state:
        st.divider()
        st.subheader("AI Analysis")
        
        if st.button("🤖 Generate Brand Report", type="primary"):
            df = st.session_state.scraped_data
            
            # Prepare comments
            comments = df['comment'].dropna().str.strip()
            comments = comments[comments != ""].head(10)
            
            if len(comments) == 0:
                st.warning("No valid comments for analysis")
            else:
                # Build prompt
                prompt = f"""Analyze brand sentiment for {keyword}:

**Comments:**
""" + "\n".join(f"- {c}" for c in comments) + """

**Analysis Requirements:**
1. Overall sentiment (Positive/Neutral/Negative)
2. Top 3 strengths
3. Top 3 weaknesses
4. 50-word summary
5. 3 improvement suggestions"""

                with st.spinner("Generating report..."):
                    try:
                        response = run_gpt_prompt(prompt)
                        st.success("Done! Here's your brand report:")
                        st.markdown(response)
                        
                        # Export
                        if st.download_button("📥 Download Report",
                                            response,
                                            file_name=f"{keyword}_brand_report.txt"):
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
