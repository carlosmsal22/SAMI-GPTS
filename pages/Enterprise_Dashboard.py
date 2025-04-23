import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from utils.gpt_scraper import EnterpriseScraper
from utils.gpt_helpers import run_gpt_prompt

def show_debug_info(data):
    with st.expander("🛠️ Debug Information"):
        st.write("### Raw Data Sample")
        st.json(data[:2], expanded=False)
        
        st.write("### Data Statistics")
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            st.write(f"Total mentions: {len(df)}")
            st.write(f"Sources: {df['source'].unique().tolist()}")
            st.write(f"Date range: {df['date'].min()} to {df['date'].max()}")
        else:
            st.warning("No valid data structure")

def main():
    st.set_page_config(layout="wide", page_title="EnterpriseIQ")
    st.title("🚀 Enterprise Intelligence Dashboard")
    
    # Configuration
    company = st.text_input("Company Name", "Apple")
    analysis_type = st.radio(
        "Analysis Type",
        ["Quick Scan", "Comprehensive Report"],
        horizontal=True
    )
    
    if st.button("🔍 Analyze Company"):
        with st.spinner(f"Analyzing {company}..."):
            try:
                scraper = EnterpriseScraper()
                
                # Data collection
                data = scraper.scrape_enterprise_data(company)
                if not data:
                    st.error("""
                    No data found. This could be because:
                    - The company has limited online presence
                    - Temporary scraping limitations
                    - Try alternative company names (e.g., 'AAPL' for Apple)
                    """)
                    show_debug_info(data)
                    return
                
                # Analysis
                analysis = scraper.analyze_sentiment(data)
                if 'error' in analysis:
                    st.error(f"Analysis failed: {analysis['error']}")
                    show_debug_info(data)
                    return
                
                # Display results
                st.success(f"✅ Analyzed {len(data)} mentions")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Overall Score", f"{analysis.get('overall_score', 'N/A')}/10")
                with col2:
                    st.metric("Positive Sentiment", f"{analysis.get('sentiment_breakdown', {}).get('positive', 0)}%")
                
                # Visualizations
                if 'sentiment_breakdown' in analysis:
                    fig = px.pie(
                        values=list(analysis['sentiment_breakdown'].values()),
                        names=list(analysis['sentiment_breakdown'].keys()),
                        title="Sentiment Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed findings
                with st.expander("📊 Key Findings"):
                    if 'top_strengths' in analysis:
                        st.write("### ✅ Strengths")
                        for strength in analysis['top_strengths']:
                            st.markdown(f"- {strength}")
                    
                    if 'top_weaknesses' in analysis:
                        st.write("### ⚠️ Weaknesses")
                        for weakness in analysis['top_weaknesses']:
                            st.markdown(f"- {weakness}")
                
                # Debug info
                show_debug_info(data)
                
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()
