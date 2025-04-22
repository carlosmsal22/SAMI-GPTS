import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt
import sys
import os
from pathlib import Path

# Configure paths
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Debugging setup
DEBUG = True  # Set to False in production

def main():
    st.set_page_config(page_title="Brand Analyzer", layout="wide")
    st.title("🧠 Scrape + Analyze Brand Reputation")
    
    # Input Section
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Enter a brand (e.g. Nike, Apple)", key="brand_input")
    with col2:
        num = st.slider("Number of posts/reviews", 5, 50, 10, key="num_slider")
    
    # Scraping Section
    if st.button("🚀 Scrape the Web", key="scrape_btn"):
        if not keyword:
            st.warning("Please enter a brand name first!")
            return
            
        with st.spinner(f"Scraping data for {keyword}..."):
            try:
                reddit_df = scrape_reddit(keyword, max_posts=num)
                trust_df = scrape_trustpilot(keyword, max_reviews=num)
                
                if DEBUG:
                    st.write("Raw Reddit Data:", reddit_df)
                    st.write("Raw Trustpilot Data:", trust_df)
                
                # Standardize data
                dfs = []
                for df, source in [(reddit_df, "Reddit"), (trust_df, "Trustpilot")]:
                    if not df.empty:
                        # Handle different column names
                        comment_col = next((col for col in df.columns if 'comment' in col.lower() or 'text' in col.lower() or 'title' in col.lower()), None)
                        if comment_col:
                            df = df.rename(columns={comment_col: 'comment'})
                            dfs.append(df)
                        else:
                            st.warning(f"No comments found in {source} data")
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.scraped_data = full_df
                    st.success(f"✅ Successfully scraped {len(full_df)} comments!")
                    
                    # Show sample data
                    with st.expander("View Scraped Data"):
                        st.dataframe(full_df)
                        
                    # Show statistics
                    st.metric("Total Comments", len(full_df))
                    st.metric("Sources", ", ".join(full_df['source'].unique()))
                else:
                    st.error("⚠️ No valid data found from any source")
                    if DEBUG:
                        st.json({
                            "Reddit Columns": list(reddit_df.columns) if not reddit_df.empty else "Empty",
                            "Trustpilot Columns": list(trust_df.columns) if not trust_df.empty else "Empty"
                        })
                        
            except Exception as e:
                st.error(f"🔥 Scraping failed: {str(e)}")
                if DEBUG:
                    st.exception(e)

    # Analysis Section
    if "scraped_data" in st.session_state and st.session_state.scraped_data is not None:
        st.divider()
        st.subheader("GPT Analysis")
        
        if st.button("🧠 Analyze with GPT", key="analyze_btn"):
            df = st.session_state.scraped_data
            
            try:
                # Validate data
                if 'comment' not in df.columns:
                    st.error("Data format error: No 'comment' column found")
                    st.write("Available columns:", df.columns.tolist())
                    return
                
                comments = df['comment'].dropna().head(10)
                if len(comments) == 0:
                    st.warning("No valid comments found for analysis")
                    return
                
                # Build prompt
                prompt = f"""Analyze brand sentiment for {keyword} based on these comments:

1. Overall Sentiment (Positive/Negative/Neutral)
2. Top 3 Positive Aspects
3. Top 3 Complaints
4. Reputation Summary (50 words)

Comments:
""" + "\n".join(f"- {c[:200]}" for c in comments)  # Truncate long comments

                st.code(prompt, language="text")
                
                with st.spinner("🔍 Analyzing with GPT..."):
                    response = run_gpt_prompt(
                        prompt,
                        model="gpt-4",
                        module="brand_reputation"
                    )
                
                st.success("Analysis Complete!")
                st.markdown("### 📝 Brand Reputation Report")
                st.write(response)
                
                # Optional: Save results
                if st.button("💾 Save Report"):
                    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{keyword}_analysis_{timestamp}.txt"
                    with open(filename, "w") as f:
                        f.write(response)
                    st.success(f"Report saved as {filename}")
                    
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                if DEBUG:
                    st.exception(e)
    else:
        st.info("👆 Please scrape data first to enable analysis")

if __name__ == "__main__":
    main()
