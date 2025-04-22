import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_cybersecurity_forums, scrape_tech_review_sites, scrape_news_mentions
from utils.gpt_helpers import run_gpt_prompt
import sys
from pathlib import Path

# Configure paths
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(page_title="Secureonix Analyzer", layout="wide")
    st.title("🔒 Secureonix Reputation Analysis")
    
    # Input Section
    keyword = "Secureonix"  # Fixed for this analysis
    num = st.slider("Number of sources to analyze", 5, 50, 15)
    
    if st.button("🔍 Collect Security Community Feedback", type="primary"):
        with st.spinner(f"Gathering cybersecurity community insights about {keyword}..."):
            try:
                # Get data from multiple technical sources
                forum_df = scrape_cybersecurity_forums(keyword, max_posts=num//2)
                review_df = scrape_tech_review_sites(keyword, max_reviews=num//2)
                news_df = scrape_news_mentions(keyword, max_articles=5)
                
                # Combine data
                dfs = []
                for df, name in [(forum_df, "Forums"), (review_df, "Reviews"), (news_df, "News")]:
                    if not df.empty:
                        dfs.append(df)
                        st.success(f"Found {len(df)} {name} mentions")
                
                if dfs:
                    full_df = pd.concat(dfs, ignore_index=True)
                    st.session_state.scraped_data = full_df
                    
                    with st.expander("View Collected Data"):
                        st.dataframe(full_df.sort_values('date', ascending=False))
                else:
                    st.warning("""
                    No technical discussions found. This could mean:
                    - Secureonix is a newer/niche player
                    - Enterprise solutions get less public discussion
                    - Try alternative spellings (SecureOnix, Secure-Onix)
                    """)
                    
            except Exception as e:
                st.error(f"Data collection error: {str(e)}")

    # Analysis Section
    if "scraped_data" in st.session_state:
        st.divider()
        st.subheader("Cybersecurity Expert Analysis")
        
        if st.button("🛡️ Generate Security Industry Report", type="primary"):
            df = st.session_state.scraped_data
            
            # Prepare specialized cybersecurity prompt
            prompt = f"""As a cybersecurity analyst, evaluate Secureonix's reputation:

**Data Sources:**
{df['source'].value_counts().to_string()}

**Key Mentions:**
""" + "\n".join(f"- {row['comment'][:150]}... ({row['source']})" 
              for _, row in df.head(10).iterrows()) + """

**Analysis Requirements:**
1. Enterprise Security Perception (1-5 scale)
2. Top 3 Strengths (technical capabilities)
3. Top 3 Weaknesses (based on feedback)
4. Competitive Positioning vs. CrowdStrike/Palo Alto
5. Recommended Improvements (technical & business)
6. 50-word Executive Summary"""

            with st.spinner("Generating expert analysis..."):
                try:
                    response = run_gpt_prompt(
                        prompt,
                        model="gpt-4",
                        temperature=0.3,  # More factual
                        max_tokens=800
                    )
                    st.success("Cybersecurity Analysis Complete!")
                    st.markdown(response)
                    
                    # Export as markdown
                    st.download_button(
                        "📄 Download Full Report",
                        data=response,
                        file_name="secureonix_cybersecurity_analysis.md"
                    )
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
